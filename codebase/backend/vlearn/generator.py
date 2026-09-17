"""Pipeline generate bộ câu hỏi cho một Day cụ thể.

Luồng: transcript index -> chọn đoạn nguồn -> gọi LLM (hoặc mock offline) ->
parse JSON -> VALIDATE mã trích dẫn (bắt buộc, "trung thực với nguồn") ->
retry tối đa N lần cho câu lỗi (chế độ live) -> loại câu không cứu được ->
lưu DB + export CSV/MD.
"""
from __future__ import annotations

import random
from typing import Any

from vlearn import config, db, llm
from vlearn.errors import VlearnError
from vlearn.transcript_index import TranscriptIndex

DEFAULT_NUM_QUESTIONS = 10
DEFAULT_MCQ_RATIO = 0.4
DEFAULT_MAX_RETRIES = 2


def _short(text: str, limit: int = 160) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def _select_source_codes(index: TranscriptIndex, num_questions: int) -> list[str]:
    order = index.order
    n = len(order)
    if n == 0:
        raise VlearnError(f"Transcript '{index.file_path.name}' không có đoạn nào để sinh câu hỏi.")
    if num_questions <= 0:
        raise VlearnError("num_questions phải > 0.")
    if num_questions >= n:
        return list(order)
    step = n / num_questions
    picked = [order[int(i * step)] for i in range(num_questions)]
    return list(dict.fromkeys(picked))  # giữ thứ tự, loại trùng phòng khi step < 1 do làm tròn


def _validate_question_shape(
    q: dict[str, Any], index: TranscriptIndex, *, expected_code: str | None = None
) -> tuple[bool, str]:
    """Kiểm tra hình dạng câu hỏi + validate mã trích dẫn (lớp trung thực với nguồn)."""
    if not isinstance(q, dict):
        return False, "câu hỏi không phải object JSON hợp lệ"
    qtype = q.get("qtype")
    if qtype not in {"mcq", "text"}:
        return False, f"qtype không hợp lệ: {qtype!r}"
    for key in ("question", "answer", "explain", "reference_code", "reference_quote"):
        if not q.get(key):
            return False, f"thiếu field bắt buộc '{key}'"

    combined_text = " ".join(
        str(q.get(k, "")) for k in ("question", "answer", "explain", "reference_quote", "reference_code")
    )
    valid_codes, invalid_codes = index.validate_codes(combined_text)
    if invalid_codes:
        return False, f"chứa mã bịa (không tồn tại trong transcript): {invalid_codes}"
    if not valid_codes:
        return False, "không có mã trích dẫn hợp lệ nào trong câu hỏi"

    ref_code = q.get("reference_code")
    if ref_code not in index.code_map:
        return False, f"reference_code '{ref_code}' không tồn tại trong transcript"
    if expected_code and ref_code != expected_code:
        return False, f"reference_code '{ref_code}' khác mã được yêu cầu '{expected_code}'"

    if qtype == "mcq":
        options = q.get("options")
        correct_key = q.get("correct_key")
        if not isinstance(options, list) or len(options) != 4:
            return False, "câu mcq phải có đúng 4 lựa chọn"
        if correct_key not in ("A", "B", "C", "D"):
            return False, f"correct_key không hợp lệ: {correct_key!r}"

    return True, ""


# ---------------------------------------------------------------------------
# Chế độ OFFLINE — mock deterministic, dựng thẳng từ transcript thật (mã thật)
# ---------------------------------------------------------------------------
def _mock_generate(index: TranscriptIndex, day: int, num_questions: int, mcq_ratio: float) -> list[dict[str, Any]]:
    codes = _select_source_codes(index, num_questions)
    num_mcq = round(len(codes) * mcq_ratio)
    # Seed cố định theo day -> kết quả offline lặp lại y hệt giữa các lần chạy (dễ demo/test).
    rng = random.Random(20260917 + day)

    questions: list[dict[str, Any]] = []
    for i, code in enumerate(codes):
        text = index.get(code) or ""
        if i < num_mcq:
            distractor_pool = [c for c in index.order if c != code]
            rng.shuffle(distractor_pool)
            distractors = distractor_pool[:3]
            option_codes = [code] + distractors
            rng.shuffle(option_codes)
            correct_key = "ABCD"[option_codes.index(code)]
            options = [_short(index.get(c) or "") for c in option_codes]
            questions.append(
                {
                    "qtype": "mcq",
                    "question": (
                        f"Theo bài giảng Day {day}, nội dung nào sau đây mô tả ĐÚNG nhất "
                        f"phần được trích tại {code}?"
                    ),
                    "options": options,
                    "correct_key": correct_key,
                    "answer": _short(text),
                    "explain": f"Đáp án đúng là phương án {correct_key}, trích trực tiếp từ {code} trong transcript.",
                    "reference_code": code,
                    "reference_quote": text,
                }
            )
        else:
            hint_words = " ".join(text.split()[:10])
            questions.append(
                {
                    "qtype": "text",
                    "question": (
                        f"Hãy trình bày lại bằng lời của bạn nội dung được giảng ở Day {day} "
                        f'(gợi ý, đoạn liên quan bắt đầu bằng: "{hint_words}..."):'
                    ),
                    "answer": _short(text, 400),
                    "explain": f"Đáp án mẫu được trích trực tiếp từ transcript tại {code}.",
                    "reference_code": code,
                    "reference_quote": text,
                }
            )
    return questions


# ---------------------------------------------------------------------------
# Chế độ LIVE — gọi LLM thật qua providers/, có retry cho câu lỗi mã trích dẫn
# ---------------------------------------------------------------------------
def _live_generate(
    index: TranscriptIndex, day: int, num_questions: int, mcq_ratio: float, max_retries: int
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    codes = _select_source_codes(index, num_questions)
    system_prompt = llm.load_prompt("generate_quiz.md")
    num_mcq = round(len(codes) * mcq_ratio)
    num_text = len(codes) - num_mcq
    allowed_codes = ", ".join(codes)
    context_block = index.as_context_block(codes)

    base_prompt = (
        f"Day: {day}\n"
        f"Sinh đúng {len(codes)} câu hỏi: {num_mcq} câu trắc nghiệm (qtype=mcq) và "
        f"{num_text} câu tự luận (qtype=text).\n"
        "Mỗi câu PHẢI dùng một mã khác nhau trong 'Danh sách mã được phép dùng' dưới đây, "
        "mỗi mã dùng cho đúng một câu, không dùng mã nào ngoài danh sách.\n\n"
        f"Danh sách mã được phép dùng: {allowed_codes}\n\n"
        f"Nội dung transcript (mã: nội dung):\n{context_block}\n"
    )

    collected: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []
    remaining = list(codes)
    attempt = 0
    while remaining and attempt <= max_retries:
        attempt += 1
        prompt = base_prompt
        if attempt > 1:
            prompt += (
                f"\n(Lượt thử lại {attempt}: CHỈ sinh câu hỏi cho các mã còn thiếu/bị lỗi ở lượt trước: "
                f"{', '.join(remaining)})"
            )
        try:
            data = llm.call_llm_json(system_prompt, prompt)
        except VlearnError as exc:
            warnings.append(f"Lượt {attempt}: lỗi gọi LLM — {exc}")
            break

        raw_questions = data.get("questions", []) if isinstance(data, dict) else []
        still_missing = []
        for code in remaining:
            match = next(
                (q for q in raw_questions if isinstance(q, dict) and q.get("reference_code") == code), None
            )
            if match is None:
                still_missing.append(code)
                continue
            ok, reason = _validate_question_shape(match, index, expected_code=code)
            if ok:
                collected[code] = match
            else:
                warnings.append(f"{code} (lượt {attempt}): {reason}")
                still_missing.append(code)
        remaining = still_missing

    if remaining:
        warnings.append(f"Bỏ {len(remaining)} câu không cứu được sau {attempt} lượt thử: {remaining}")

    ordered_questions = [collected[c] for c in codes if c in collected]
    return ordered_questions, remaining, warnings


# ---------------------------------------------------------------------------
# Entry point dùng chung cho CLI + API
# ---------------------------------------------------------------------------
def generate_for_day(
    day: int,
    *,
    num_questions: int = DEFAULT_NUM_QUESTIONS,
    mcq_ratio: float = DEFAULT_MCQ_RATIO,
    regenerate: bool = False,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> dict[str, Any]:
    db.init_db()
    index = TranscriptIndex.load(day)

    removed = db.delete_questions_for_day(day) if regenerate else 0

    mode = "offline" if llm.is_offline() else "live"
    dropped: list[str] = []
    warnings: list[str] = []
    if mode == "offline":
        raw_questions = _mock_generate(index, day, num_questions, mcq_ratio)
    else:
        raw_questions, dropped, warnings = _live_generate(index, day, num_questions, mcq_ratio, max_retries)

    transcript_rel = str(index.file_path.relative_to(config.REPO_ROOT))
    saved_ids: list[str] = []
    for q in raw_questions:
        # Chốt chặn cuối cùng trước khi ghi DB — validate lại dù offline hay live.
        ok, reason = _validate_question_shape(q, index)
        if not ok:
            dropped.append(q.get("reference_code", "?"))
            warnings.append(f"Loại câu hỏi ở bước lưu DB (không qua kiểm tra cuối): {reason}")
            continue
        reference_url = db.reference_url_for(transcript_rel, q["reference_code"])
        qid = db.insert_question(
            day=day,
            qtype=q["qtype"],
            question=q["question"],
            answer=q["answer"],
            explain=q["explain"],
            reference=q["reference_quote"],
            reference_code=q["reference_code"],
            reference_url=reference_url,
            options=q.get("options"),
            correct_key=q.get("correct_key"),
        )
        saved_ids.append(qid)

    csv_path = db.export_csv(day)
    md_path = db.export_md(day)

    return {
        "day": day,
        "mode": mode,
        "requested": num_questions,
        "generated": len(saved_ids),
        "dropped_reference_codes": dropped,
        "warnings": warnings,
        "removed_existing": removed,
        "question_ids": saved_ids,
        "csv_path": str(csv_path.relative_to(config.REPO_ROOT)),
        "md_path": str(md_path.relative_to(config.REPO_ROOT)),
    }
