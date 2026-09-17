"""HTTP API cho sản phẩm "Học từ lỗi trước" (D2 VLearn quiz).

Chạy: `python api.py` (mặc định cổng 8000) hoặc `python vlearn_cli.py serve`.
Phục vụ luôn `codebase/index.html` tại "/" (static, KHÔNG sửa nội dung) để
tiện demo — index.html hiện là prototype tĩnh, chưa gọi API này.

Xem README_VLEARN.md để biết đầy đủ bảng endpoint + ví dụ request/response.
"""
from __future__ import annotations

import re
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from vlearn import config, db, generator, grader, ingest, llm
from vlearn.errors import VlearnError
from vlearn.transcript_index import TranscriptIndex

app = FastAPI(
    title="VLearn Quiz API — Học từ lỗi trước",
    description="Backend + AI cho quiz sinh từ transcript bài giảng, chấm bài có trích dẫn nguồn.",
    version="0.1.0",
)

# CORS mở cho localhost (mọi cổng) — đủ dùng cho demo frontend chạy local.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(VlearnError)
async def handle_vlearn_error(request, exc: VlearnError):  # noqa: ANN001 — kiểu của request do FastAPI quyết định
    return JSONResponse(status_code=400, content={"error": str(exc)})


@app.on_event("startup")
def on_startup() -> None:
    config.ensure_output_dirs()
    db.init_db()


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
class IngestRequest(BaseModel):
    day: int = Field(..., ge=1, le=99, description="Số thứ tự ngày học, vd 1")


class GenerateRequest(BaseModel):
    day: int = Field(..., ge=1, le=99)
    num_questions: int = Field(default=generator.DEFAULT_NUM_QUESTIONS, ge=1, le=50)
    mcq_ratio: float = Field(default=generator.DEFAULT_MCQ_RATIO, ge=0.0, le=1.0)
    regenerate: bool = Field(default=False, description="Xoá bộ câu hỏi cũ của day này trước khi sinh lại")


class AnswerRequest(BaseModel):
    question_id: str
    user_answer: str = ""


class SubmitRequest(BaseModel):
    day: int = Field(..., ge=1, le=99)
    attempt_id: str | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "mode": llm.SETTINGS.mode,
        "provider": llm.SETTINGS.provider_name,
        "model": llm.SETTINGS.model,
    }


_SLIDE_DAY_RE = re.compile(r"^d(?:ay)?0*(\d+)", re.IGNORECASE)


@app.get("/api/days")
def list_days() -> list[dict]:
    days: set[int] = set()
    slide_by_day: dict[int, str] = {}
    if config.SLIDES_DIR.exists():
        for pdf_path in sorted(config.SLIDES_DIR.glob("*.pdf")):
            match = _SLIDE_DAY_RE.match(pdf_path.stem)
            if match:
                day_num = int(match.group(1))
                days.add(day_num)
                slide_by_day.setdefault(day_num, pdf_path.name)

    raw_index = ingest.load_transcript_index_raw()
    for key in raw_index:
        try:
            days.add(int(key))
        except ValueError:
            continue

    conn = db.get_connection()
    try:
        rows = conn.execute("SELECT DISTINCT day FROM questions").fetchall()
    finally:
        conn.close()
    for row in rows:
        days.add(int(row["day"]))

    result = []
    for day_num in sorted(days):
        transcript_path = config.TRANSCRIPT_DIR / f"transcript-{day_num:02d}-clean.md"
        entry = raw_index.get(str(day_num), {})
        num_questions = db.count_questions_for_day(day_num)
        result.append(
            {
                "day": day_num,
                "has_slide": day_num in slide_by_day,
                "slide_file": slide_by_day.get(day_num),
                "has_transcript": transcript_path.exists(),
                "transcript_file": entry.get("transcript_file"),
                "num_segments": entry.get("num_segments"),
                "has_quiz": num_questions > 0,
                "num_questions": num_questions,
            }
        )
    return result


_ALLOWED_UPLOAD_SUFFIX = ".pdf"


@app.post("/api/upload")
async def api_upload(file: UploadFile = File(...)) -> JSONResponse:
    """Nhận 1 file PDF slide bài giảng từ màn hình import, lưu vào data/slides/.

    Chỉ nhận .pdf (khớp pipeline ingest hiện tại — pypdf). Tên file càng khớp
    quy ước 'd<N>-...pdf' / 'day<N>-...pdf' thì càng tự nhận diện được Day N
    (dùng chung regex với GET /api/days) — nếu không khớp, vẫn lưu file
    nhưng trả `day: null` kèm hướng dẫn đặt tên lại.
    """
    original_name = file.filename or "upload.pdf"
    suffix = Path(original_name).suffix.lower()
    if suffix != _ALLOWED_UPLOAD_SUFFIX:
        return JSONResponse(
            status_code=400,
            content={"error": f"Chỉ nhận file .pdf — file '{original_name}' không hợp lệ."},
        )

    content = await file.read()
    if not content:
        return JSONResponse(status_code=400, content={"error": "File rỗng — vui lòng chọn lại file PDF."})

    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", original_name).strip("_") or "upload.pdf"
    config.SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    dest = config.SLIDES_DIR / safe_name
    dest.write_bytes(content)

    match = _SLIDE_DAY_RE.match(dest.stem)
    day = int(match.group(1)) if match else None
    if day is not None:
        message = f"Đã lưu '{dest.name}' vào data/slides/. Tự nhận diện Day {day}."
    else:
        message = (
            f"Đã lưu '{dest.name}' vào data/slides/. Không tự nhận diện được ngày học từ tên file — "
            "đặt tên theo dạng 'd<N>-...pdf' để hệ thống tự nhận, hoặc tự nhập đúng số ngày ở bước Generate."
        )
    return JSONResponse(content={"filename": dest.name, "day": day, "message": message})


@app.post("/api/ingest")
def api_ingest(body: IngestRequest) -> dict:
    return ingest.ingest_day(body.day)


@app.post("/api/generate")
def api_generate(body: GenerateRequest) -> dict:
    return generator.generate_for_day(
        body.day,
        num_questions=body.num_questions,
        mcq_ratio=body.mcq_ratio,
        regenerate=body.regenerate,
    )


def _public_question(q: dict) -> dict:
    """Loại bỏ answer/explain/correct_key trước khi trả cho UI làm bài."""
    return {
        "id": q["id"],
        "day": q["day"],
        "qtype": q["qtype"],
        "question": q["question"],
        "options": q.get("options"),
    }


@app.get("/api/quiz/{day}")
def api_quiz(day: int) -> list[dict]:
    questions = db.get_questions_for_day(day)
    return [_public_question(q) for q in questions]


@app.post("/api/answer")
def api_answer(body: AnswerRequest) -> dict:
    return grader.grade_answer(body.question_id, body.user_answer)


@app.get("/api/summary/{day}")
def api_summary(day: int) -> dict:
    return db.summary_for_day(day)


@app.post("/api/submit")
def api_submit(body: SubmitRequest) -> dict:
    return db.summary_for_day(body.day)


@app.get("/api/transcript/{day}/{code}")
def api_transcript_code(day: int, code: str) -> dict:
    normalized = code if code.startswith("[") else f"[{code}]"
    index = TranscriptIndex.load(day)
    text = index.get(normalized)
    if text is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Không tìm thấy mã '{normalized}' trong transcript Day {day}."},
        )
    return {"day": day, "code": normalized, "text": text}


# ---------------------------------------------------------------------------
# Static demo — phục vụ codebase/index.html tại "/" (không sửa nội dung file)
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    return FileResponse(str(config.INDEX_HTML_PATH))


def main() -> None:
    import os

    import uvicorn

    port = int(os.getenv("VLEARN_PORT", "8000"))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
