"""Trích xuất transcript có mã đoạn [Txx-NNN] từ slide PDF trong data/slides/.

Quy ước mã: Day N -> prefix "T" + 2 chữ số của N (Day 1 -> "T01"), số thứ tự
đoạn NNN đánh tăng dần từ 001, zero-pad 3 chữ số trong phạm vi MỘT ngày học.

Hỗ trợ 2 nguồn:
1. Sinh mới từ PDF trong data/slides/ (dùng pypdf) khi chưa có transcript.
2. Người dùng tự thả sẵn file `transcript-<XX>-clean.md` vào output/transcript/
   (ví dụ transcript gốc thật của khoá học) -> ingest sẽ CHỈ đọc để lập
   index.json, KHÔNG ghi đè nội dung đã có.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from vlearn import config
from vlearn.errors import VlearnError
from vlearn.transcript_index import parse_transcript_text

# Các dòng lặp lại trên mọi trang (header/footer slide) — coi là rác, loại bỏ
# khỏi transcript vì không mang nội dung bài giảng.
NOISE_LINE_PATTERNS = [
    re.compile(r"^AI IN ACTION\b", re.IGNORECASE),
    re.compile(r"^\d+$"),  # số trang đứng riêng một dòng
    re.compile(r"^Trang\s*\d+\s*/\s*\d+$", re.IGNORECASE),
]

BULLET_PREFIX_RE = re.compile(r"^[•\-•●▪]\s*")
NUMBERED_PREFIX_RE = re.compile(r"^\d+[\.\)]\s+")

MIN_SEGMENT_LEN = 8  # bỏ các đoạn quá ngắn (tiêu đề trơ trọi, rác OCR...)


def day_to_prefix(day: int) -> str:
    """Day N -> prefix mã 'T' + 2 chữ số, vd Day 1 -> 'T01'."""
    if day <= 0 or day > 99:
        raise VlearnError(f"Số ngày học (day={day}) không hợp lệ — phải trong khoảng 1..99.")
    return f"T{day:02d}"


def transcript_filename(day: int) -> str:
    return f"transcript-{day:02d}-clean.md"


def find_slide_for_day(day: int) -> Path | None:
    """Tìm file slide PDF tương ứng với Day N trong data/slides/.

    Chấp nhận các cách đặt tên phổ biến: 'd1-...pdf', 'd01-...pdf',
    'day1-...pdf', 'day01-...pdf' (không phân biệt hoa/thường).
    """
    if not config.SLIDES_DIR.exists():
        return None
    patterns = [
        re.compile(rf"^d0*{day}([^0-9].*)?$", re.IGNORECASE),
        re.compile(rf"^day0*{day}([^0-9].*)?$", re.IGNORECASE),
    ]
    matches = []
    for pdf_path in sorted(config.SLIDES_DIR.glob("*.pdf")):
        stem = pdf_path.stem
        if any(p.match(stem) for p in patterns):
            matches.append(pdf_path)
    return matches[0] if matches else None


def _is_noise_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    return any(pattern.match(stripped) for pattern in NOISE_LINE_PATTERNS)


def _page_to_segments(raw_text: str) -> list[str]:
    """Chuyển text thô của một trang slide thành các đoạn (segment) ngắn.

    Heuristic đơn giản: mỗi bullet ("•", "-", "1.") là một segment riêng;
    các dòng không phải bullet được gộp lại thành một segment "ngữ cảnh".
    """
    lines = [ln.strip() for ln in raw_text.split("\n")]
    lines = [ln for ln in lines if not _is_noise_line(ln)]

    segments: list[str] = []
    buffer: list[str] = []

    def flush_buffer() -> None:
        if buffer:
            text = " ".join(buffer).strip()
            if text:
                segments.append(text)
            buffer.clear()

    for line in lines:
        if BULLET_PREFIX_RE.match(line) or NUMBERED_PREFIX_RE.match(line):
            flush_buffer()
            cleaned = BULLET_PREFIX_RE.sub("", line)
            cleaned = NUMBERED_PREFIX_RE.sub("", cleaned)
            segments.append(cleaned.strip())
        else:
            buffer.append(line)
    flush_buffer()

    return [s for s in segments if len(s) >= MIN_SEGMENT_LEN]


def _extract_segments_from_pdf(pdf_path: Path) -> list[tuple[int, str]]:
    """Trả về list (số trang slide, nội dung đoạn) theo đúng thứ tự trong PDF."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise VlearnError(
            "Thiếu thư viện 'pypdf' để đọc file PDF. "
            "Cài đặt bằng lệnh: pip install pypdf  (hoặc: pip install -r codebase/backend/requirements.txt)"
        ) from exc

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:  # file hỏng / không phải PDF hợp lệ
        raise VlearnError(f"Không đọc được file PDF '{pdf_path.name}': {exc}") from exc

    result: list[tuple[int, str]] = []
    for page_index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # một số trang PDF có thể lỗi cục bộ
            text = ""
            print(f"[vlearn.ingest] Cảnh báo: không trích xuất được text ở trang {page_index}: {exc}")
        for segment in _page_to_segments(text):
            result.append((page_index, segment))
    return result


def _write_transcript_markdown(
    *, day: int, source_slide_name: str, segments: list[tuple[int, str]], out_path: Path
) -> int:
    prefix = day_to_prefix(day)
    lines: list[str] = [
        f"# Transcript Day {day} (tự sinh từ slide)",
        "",
        f"> Sinh tự động bởi `vlearn/ingest.py` từ file slide `{source_slide_name}`. "
        "Đây là bản trích xuất theo cấu trúc SLIDE (không phải transcript giọng nói gốc của giảng viên) "
        "— dùng làm nguồn trích dẫn khi chưa có transcript thật của khoá học.",
        "",
    ]
    current_page = None
    counter = 0
    for page_index, segment_text in segments:
        counter += 1
        code = f"[{prefix}-{counter:03d}]"
        if page_index != current_page:
            lines.append(f"## Slide {page_index}")
            lines.append("")
            current_page = page_index
        lines.append(f"{code} {segment_text}")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return counter


def _update_index_entry(day: int, entry: dict[str, Any]) -> None:
    config.ensure_output_dirs()
    index_data: dict[str, Any] = {}
    if config.TRANSCRIPT_INDEX_FILE.exists():
        try:
            index_data = json.loads(config.TRANSCRIPT_INDEX_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            index_data = {}
    index_data[str(day)] = entry
    config.TRANSCRIPT_INDEX_FILE.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def load_transcript_index_raw() -> dict[str, Any]:
    if not config.TRANSCRIPT_INDEX_FILE.exists():
        return {}
    try:
        return json.loads(config.TRANSCRIPT_INDEX_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def ingest_day(day: int, *, force: bool = False) -> dict[str, Any]:
    """Trích xuất transcript cho một Day cụ thể.

    - Nếu output/transcript/transcript-<XX>-clean.md ĐÃ TỒN TẠI và force=False:
      không ghi đè, chỉ đọc lại để cập nhật index.json (trường hợp người dùng
      tự thả sẵn transcript thật vào thư mục này).
    - Ngược lại: tìm slide PDF tương ứng trong data/slides/, trích xuất và ghi
      file transcript mới.
    """
    config.ensure_output_dirs()
    out_path = config.TRANSCRIPT_DIR / transcript_filename(day)
    prefix = day_to_prefix(day)

    if out_path.exists() and not force:
        text = out_path.read_text(encoding="utf-8")
        code_map, order, duplicates = parse_transcript_text(text)
        if duplicates:
            print(f"[vlearn.ingest] Cảnh báo: mã trích dẫn lặp trong {out_path.name}: {duplicates}")
        entry = {
            "transcript_file": str(out_path.relative_to(config.REPO_ROOT)),
            "code_prefix": prefix,
            "num_segments": len(order),
            "source_slide": "da_co_san_trong_output_transcript",
            "ingested_at": datetime.now().isoformat(timespec="seconds"),
        }
        _update_index_entry(day, entry)
        return {
            "day": day,
            "skipped_existing": True,
            "message": (
                f"Đã có sẵn '{out_path.name}' trong output/transcript/ — không ghi đè. "
                f"Đã đọc lại và cập nhật index.json ({len(order)} đoạn)."
            ),
            **entry,
        }

    slide_path = find_slide_for_day(day)
    if slide_path is None:
        raise VlearnError(
            f"Không tìm thấy file slide cho Day {day} trong '{config.SLIDES_DIR}'. "
            f"Đặt file dạng 'd{day}-<tên>.pdf' hoặc 'day{day}-<tên>.pdf' vào thư mục đó, "
            "hoặc tự thả sẵn transcript vào output/transcript/ theo tên "
            f"'{transcript_filename(day)}'."
        )

    segments = _extract_segments_from_pdf(slide_path)
    if not segments:
        raise VlearnError(
            f"Trích xuất từ '{slide_path.name}' không ra được đoạn nội dung nào. "
            "File PDF có thể là ảnh scan (không có text layer) — cần OCR trước, "
            "hoặc kiểm tra lại file."
        )

    num_segments = _write_transcript_markdown(
        day=day, source_slide_name=slide_path.name, segments=segments, out_path=out_path
    )
    entry = {
        "transcript_file": str(out_path.relative_to(config.REPO_ROOT)),
        "code_prefix": prefix,
        "num_segments": num_segments,
        "source_slide": str(slide_path.relative_to(config.REPO_ROOT)),
        "ingested_at": datetime.now().isoformat(timespec="seconds"),
    }
    _update_index_entry(day, entry)
    return {
        "day": day,
        "skipped_existing": False,
        "message": f"Đã sinh transcript '{out_path.name}' với {num_segments} đoạn mã [{prefix}-NNN].",
        **entry,
    }
