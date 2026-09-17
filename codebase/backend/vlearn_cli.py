"""CLI cho vlearn — dùng để demo/test không cần UI.

Ví dụ:
    python vlearn_cli.py ingest --day 1
    python vlearn_cli.py generate --day 1 --n 10
    python vlearn_cli.py show --day 1
    python vlearn_cli.py grade --question-id <id> --answer "câu trả lời của bạn"
    python vlearn_cli.py serve --port 8000
"""
from __future__ import annotations

import argparse
import json
import sys

from vlearn import config, db, generator, grader, ingest
from vlearn.errors import VlearnError


def cmd_ingest(args: argparse.Namespace) -> None:
    result = ingest.ingest_day(args.day, force=args.force)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_generate(args: argparse.Namespace) -> None:
    result = generator.generate_for_day(
        args.day,
        num_questions=args.n,
        mcq_ratio=args.mcq_ratio,
        regenerate=args.regenerate,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_show(args: argparse.Namespace) -> None:
    questions = db.get_questions_for_day(args.day)
    if not questions:
        print(f"Chưa có câu hỏi nào cho Day {args.day}. Hãy chạy 'generate --day {args.day}' trước.")
        return
    for i, q in enumerate(questions, start=1):
        print(f"\n--- Câu {i} · {q['qtype'].upper()} · id={q['id']} ---")
        print(f"Hỏi: {q['question']}")
        if q["qtype"] == "mcq" and q.get("options"):
            for key, opt in zip("ABCD", q["options"]):
                mark = " *ĐÚNG*" if key == q.get("correct_key") else ""
                print(f"  {key}. {opt}{mark}")
        print(f"Đáp án: {q['answer']}")
        print(f"Giải thích: {q['explain']}")
        print(f"Trích dẫn: {q['reference_code']} — {q['reference'][:160]}")
        print(f"Nguồn: {q['reference_url']}")


def cmd_grade(args: argparse.Namespace) -> None:
    result = grader.grade_answer(args.question_id, args.answer)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_serve(args: argparse.Namespace) -> None:
    import os

    import uvicorn

    os.environ.setdefault("VLEARN_PORT", str(args.port))
    uvicorn.run("api:app", host="0.0.0.0", port=args.port, reload=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="vlearn CLI — quiz 'Học từ lỗi trước'")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Trích xuất transcript từ slide PDF cho một Day")
    p_ingest.add_argument("--day", type=int, required=True)
    p_ingest.add_argument("--force", action="store_true", help="Ghi đè transcript đã có sẵn")
    p_ingest.set_defaults(func=cmd_ingest)

    p_generate = sub.add_parser("generate", help="Generate bộ câu hỏi cho một Day")
    p_generate.add_argument("--day", type=int, required=True)
    p_generate.add_argument("--n", type=int, default=generator.DEFAULT_NUM_QUESTIONS, help="Số câu hỏi")
    p_generate.add_argument("--mcq-ratio", type=float, default=generator.DEFAULT_MCQ_RATIO)
    p_generate.add_argument("--regenerate", action="store_true", help="Xoá bộ câu hỏi cũ trước khi sinh lại")
    p_generate.set_defaults(func=cmd_generate)

    p_show = sub.add_parser("show", help="In toàn bộ câu hỏi (kèm đáp án) của một Day — dùng để review")
    p_show.add_argument("--day", type=int, required=True)
    p_show.set_defaults(func=cmd_show)

    p_grade = sub.add_parser("grade", help="Chấm thử một câu trả lời")
    p_grade.add_argument("--question-id", required=True)
    p_grade.add_argument("--answer", required=True)
    p_grade.set_defaults(func=cmd_grade)

    p_serve = sub.add_parser("serve", help="Chạy HTTP API (FastAPI + uvicorn)")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.set_defaults(func=cmd_serve)

    return parser


def main() -> None:
    config.ensure_output_dirs()
    db.init_db()
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except VlearnError as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
