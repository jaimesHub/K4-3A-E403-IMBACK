"""Lưu trữ SQLite cho quiz — output/quiz.db.

Bảng `questions`: đúng field theo tasks.md §2.1 (id/timestamp/question/answer/
explain/reference/reference_code/reference_url) + các cột UI cần thêm
(day/qtype/options_json/correct_key).

Bảng `attempts`: kết quả làm bài, phục vụ summary cuối quiz + màn "Ôn Tập".

Kèm export ra CSV/MD (output/quiz_day<N>.csv, output/quiz_day<N>.md) để review
bằng mắt mà không cần mở DB.
"""
from __future__ import annotations

import csv
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from vlearn import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    day INTEGER NOT NULL,
    qtype TEXT NOT NULL,              -- 'mcq' | 'text'
    question TEXT NOT NULL,
    answer TEXT NOT NULL,             -- đáp án đúng (text người đọc được)
    explain TEXT NOT NULL,
    reference TEXT NOT NULL,          -- nội dung trích dẫn (nguyên văn đoạn transcript)
    reference_code TEXT NOT NULL,     -- '[Txx-NNN]'
    reference_url TEXT NOT NULL,      -- đường dẫn tới file transcript kèm anchor mã
    options_json TEXT,                -- JSON list lựa chọn (chỉ dùng cho mcq)
    correct_key TEXT                  -- 'A'/'B'/'C'/'D' (chỉ dùng cho mcq)
);

CREATE TABLE IF NOT EXISTS attempts (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    day INTEGER NOT NULL,
    question_id TEXT NOT NULL,
    user_answer TEXT NOT NULL,
    verdict_label TEXT NOT NULL,
    is_correct INTEGER NOT NULL,      -- 0/1
    explanation TEXT NOT NULL,
    reference_code TEXT,
    reference_quote TEXT,
    reference_url TEXT,
    model_used TEXT,
    invalid_codes_json TEXT,          -- mã LLM trích ra nhưng KHÔNG tồn tại thật (nếu có)
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
"""


def get_connection() -> sqlite3.Connection:
    config.ensure_output_dirs()
    conn = sqlite3.connect(str(config.DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def reference_url_for(transcript_file: str, code: str) -> str:
    """Đường dẫn tương đối (từ repo root) tới file transcript, kèm anchor mã."""
    return f"{transcript_file}#{code.strip('[]')}"


def insert_question(
    *,
    day: int,
    qtype: str,
    question: str,
    answer: str,
    explain: str,
    reference: str,
    reference_code: str,
    reference_url: str,
    options: list[str] | None = None,
    correct_key: str | None = None,
) -> str:
    if qtype not in {"mcq", "text"}:
        raise ValueError(f"qtype không hợp lệ: {qtype!r} (chỉ nhận 'mcq' hoặc 'text')")
    question_id = uuid.uuid4().hex
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO questions
                (id, timestamp, day, qtype, question, answer, explain,
                 reference, reference_code, reference_url, options_json, correct_key)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                question_id,
                datetime.now().isoformat(timespec="seconds"),
                day,
                qtype,
                question,
                answer,
                explain,
                reference,
                reference_code,
                reference_url,
                json.dumps(options, ensure_ascii=False) if options is not None else None,
                correct_key,
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return question_id


def _row_to_question_dict(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    if data.get("options_json"):
        data["options"] = json.loads(data["options_json"])
    else:
        data["options"] = None
    return data


def get_questions_for_day(day: int) -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM questions WHERE day = ? ORDER BY timestamp ASC", (day,)
        ).fetchall()
        return [_row_to_question_dict(r) for r in rows]
    finally:
        conn.close()


def get_question(question_id: str) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
        return _row_to_question_dict(row) if row else None
    finally:
        conn.close()


def count_questions_for_day(day: int) -> int:
    conn = get_connection()
    try:
        row = conn.execute("SELECT COUNT(*) AS c FROM questions WHERE day = ?", (day,)).fetchone()
        return int(row["c"])
    finally:
        conn.close()


def delete_questions_for_day(day: int) -> int:
    """Xoá toàn bộ câu hỏi (và attempts liên quan) của một Day — dùng khi regenerate."""
    conn = get_connection()
    try:
        ids = [r["id"] for r in conn.execute("SELECT id FROM questions WHERE day = ?", (day,)).fetchall()]
        if ids:
            placeholders = ",".join("?" for _ in ids)
            conn.execute(f"DELETE FROM attempts WHERE question_id IN ({placeholders})", ids)
            conn.execute(f"DELETE FROM questions WHERE id IN ({placeholders})", ids)
            conn.commit()
        return len(ids)
    finally:
        conn.close()


def insert_attempt(
    *,
    day: int,
    question_id: str,
    user_answer: str,
    verdict_label: str,
    is_correct: bool,
    explanation: str,
    reference_code: list[str] | None,
    reference_quote: list[str] | None,
    reference_url: list[str] | None,
    model_used: str | None,
    invalid_codes: list[str] | None = None,
) -> str:
    attempt_id = uuid.uuid4().hex
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO attempts
                (id, created_at, day, question_id, user_answer, verdict_label, is_correct,
                 explanation, reference_code, reference_quote, reference_url, model_used,
                 invalid_codes_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                attempt_id,
                datetime.now().isoformat(timespec="seconds"),
                day,
                question_id,
                user_answer,
                verdict_label,
                1 if is_correct else 0,
                explanation,
                json.dumps(reference_code or [], ensure_ascii=False),
                json.dumps(reference_quote or [], ensure_ascii=False),
                json.dumps(reference_url or [], ensure_ascii=False),
                model_used,
                json.dumps(invalid_codes or [], ensure_ascii=False),
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return attempt_id


def _row_to_attempt_dict(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    for key in ("reference_code", "reference_quote", "reference_url", "invalid_codes_json"):
        if data.get(key):
            try:
                data[key] = json.loads(data[key])
            except (json.JSONDecodeError, TypeError):
                pass
    return data


def get_attempts_for_day(day: int) -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM attempts WHERE day = ? ORDER BY created_at ASC", (day,)
        ).fetchall()
        return [_row_to_attempt_dict(r) for r in rows]
    finally:
        conn.close()


def get_latest_attempt_for_question(question_id: str) -> dict[str, Any] | None:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM attempts WHERE question_id = ? ORDER BY created_at DESC LIMIT 1",
            (question_id,),
        ).fetchone()
        return _row_to_attempt_dict(row) if row else None
    finally:
        conn.close()


def summary_for_day(day: int) -> dict[str, Any]:
    """Tổng kết cuối quiz: số đúng/tổng, chi tiết từng câu, trích dẫn liên quan."""
    questions = get_questions_for_day(day)
    items: list[dict[str, Any]] = []
    correct = 0
    answered = 0
    for q in questions:
        latest = get_latest_attempt_for_question(q["id"])
        item: dict[str, Any] = {
            "question_id": q["id"],
            "question": q["question"],
            "qtype": q["qtype"],
            "reference_code": q["reference_code"],
            "reference_url": q["reference_url"],
            "answered": latest is not None,
        }
        if latest is not None:
            answered += 1
            is_correct = bool(latest["is_correct"])
            if is_correct:
                correct += 1
            item.update(
                {
                    "verdict_label": latest["verdict_label"],
                    "is_correct": is_correct,
                    "explanation": latest["explanation"],
                    "attempt_reference_code": latest["reference_code"],
                    "attempt_reference_quote": latest["reference_quote"],
                    "user_answer": latest["user_answer"],
                }
            )
        items.append(item)

    total = len(questions)
    return {
        "day": day,
        "total_questions": total,
        "answered": answered,
        "correct": correct,
        "score_percent": round(correct / total * 100, 1) if total else 0.0,
        "items": items,
    }


# ---------------------------------------------------------------------------
# Export CSV / Markdown để review bằng mắt
# ---------------------------------------------------------------------------
EXPORT_FIELDS = [
    "id",
    "timestamp",
    "day",
    "qtype",
    "question",
    "answer",
    "explain",
    "reference",
    "reference_code",
    "reference_url",
    "options_json",
    "correct_key",
]


def export_csv(day: int) -> Path:
    questions = get_questions_for_day(day)
    out_path = config.OUTPUT_DIR / f"quiz_day{day}.csv"
    config.ensure_output_dirs()
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPORT_FIELDS)
        writer.writeheader()
        for q in questions:
            writer.writerow({k: q.get(k, "") for k in EXPORT_FIELDS})
    return out_path


def export_md(day: int) -> Path:
    questions = get_questions_for_day(day)
    out_path = config.OUTPUT_DIR / f"quiz_day{day}.md"
    config.ensure_output_dirs()
    lines = [f"# Bộ câu hỏi Day {day} ({len(questions)} câu)", ""]
    for i, q in enumerate(questions, start=1):
        lines.append(f"## Câu {i} · {q['qtype'].upper()} · `{q['id']}`")
        lines.append("")
        lines.append(f"**Câu hỏi:** {q['question']}")
        if q["qtype"] == "mcq" and q.get("options"):
            lines.append("")
            for key, opt in zip("ABCD", q["options"]):
                marker = " (ĐÚNG)" if key == q.get("correct_key") else ""
                lines.append(f"- **{key}.** {opt}{marker}")
        lines.append("")
        lines.append(f"**Đáp án:** {q['answer']}")
        lines.append("")
        lines.append(f"**Giải thích:** {q['explain']}")
        lines.append("")
        lines.append(f"**Trích dẫn:** {q['reference_code']} — {q['reference']}")
        lines.append("")
        lines.append(f"**Nguồn:** `{q['reference_url']}`")
        lines.append("")
        lines.append("---")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
