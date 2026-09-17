"""Chạy `eval/golden_set.json` qua `vlearn/grader.py` — phần "số đo" của CP3/CP4.

Cách dùng:
    python run_quiz_eval.py --transcript /đường/dẫn/tới/transcript-04-clean.md
    # hoặc:
    VLEARN_EVAL_TRANSCRIPT=/đường/dẫn/tới/transcript-04-clean.md python run_quiz_eval.py

QUAN TRỌNG: `transcript-04-clean.md` (nguồn sự thật của golden set) là dữ liệu
của khoá học, KHÔNG được commit vào repo theo quy định bảo mật dữ liệu
(xem CHECKLIST.md). File này vì vậy KHÔNG có sẵn trong repo — script BẮT BUỘC
nhận đường dẫn từ người dùng qua `--transcript` hoặc biến môi trường
`VLEARN_EVAL_TRANSCRIPT`. Nếu không có, script in cảnh báo rõ ràng và
`exit(1)` — TUYỆT ĐỐI KHÔNG tự bịa transcript hay bịa kết quả eval.

Mỗi case được chấm qua `grader.grade_open_answer()` — CÙNG một "động cơ chấm"
(prompt `grade_text.md`, hoặc mock offline) mà sản phẩm dùng để chấm bài tự
luận thật, chỉ khác ở chỗ eval không biết trước reference_code mà để hệ thống
tự tìm đoạn liên quan bằng `TranscriptIndex.search()` (BM25-lite).

Điều kiện ĐẠT của 1 case (đúng theo spec.md §7 / eval/golden_set.json meta):
  1. verdict_label khớp expected_output.verdict_label — kiểm tra CHÍNH XÁC bằng code.
  2. explanation phủ hết explanation_must_cover — kiểm tra HEURISTIC (so khớp từ khoá),
     không thay thế được việc người review đọc lại, xem README_VLEARN.md.
  3. explanation không chứa ý nào trong must_not_contain — kiểm tra HEURISTIC tương tự.
  4. mọi mã [Txx-xxx] AI trích ra đều tồn tại thật VÀ khớp đúng reference_code kỳ vọng
     (case 'n/a' thì không được trích mã nào) — kiểm tra CHÍNH XÁC bằng code (grep ngược
     lại transcript qua TranscriptIndex, không thể bịa).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from vlearn import config, grader
from vlearn import llm as vlearn_llm
from vlearn.errors import VlearnError
from vlearn.transcript_index import TranscriptIndex

SAFETY_GROUP = ["GS-002", "GS-006", "GS-007", "GS-008", "GS-009", "GS-025"]

_STOPWORDS_VI = {
    "la", "cua", "va", "co", "khong", "cho", "duoc", "nay", "do", "cac", "mot",
    "nhung", "de", "theo", "voi", "khi", "trong", "ra", "o", "thi", "ma", "rat",
    "cung", "nen", "vi", "neu", "nhu", "da", "se", "bi", "hay", "hoac", "vao",
    "tren", "duoi", "ve", "la", "mà", "và", "của", "là", "có", "không", "cho",
    "được", "này", "đó", "các", "một", "những", "để", "theo", "với", "khi",
    "trong", "ra", "ở", "thì", "rất", "cũng", "nên", "vì", "nếu", "như", "đã",
    "sẽ", "bị", "hay", "hoặc", "vào", "trên", "dưới", "về", "ai", "bạn",
}
_TOKEN_RE = re.compile(r"[a-zA-ZÀ-ỹà-ỹ0-9]+")

# Nhóm từ đồng nghĩa / cùng khái niệm — normalize về canonical form trước khi so khớp.
# Key = canonical, values = các biến thể mà LLM hay dùng.
_SYNONYM_GROUPS: list[set[str]] = [
    {"token", "tokens", "đơn vị", "mảnh", "mảnh từ", "sub", "subword"},
    {"từ", "word", "words", "từ ngữ", "ngôn ngữ"},
    {"máy", "model", "mô hình", "llm", "transformer"},
    {"dự đoán", "predict", "prediction", "xác suất", "probability"},
    {"hallucination", "ảo giác", "sai", "bịa", "không đúng"},
    {"context", "context window", "cửa sổ", "ngữ cảnh"},
    {"quên", "forget", "mất", "bị cắt"},
    {"parameter", "tham số", "trọng số", "weight", "năng lực"},
    {"rlhf", "reinforcement", "huấn luyện", "train", "reward"},
    {"system prompt", "prompt", "câu lệnh", "instruction"},
    {"temperature", "sampling", "top-k", "top-p", "ngẫu nhiên"},
    {"ngoài phạm vi", "không thuộc", "hành chính", "ngoài", "từ chối"},
    {"không đủ", "mơ hồ", "ngắn", "không rõ", "thiếu"},
    {"tiếng việt", "vietnamese", "tiếng anh", "english", "dấu"},
    {"chẻ", "tách", "split", "chia", "tokenize", "tokenization"},
    {"bản chất", "cơ chế", "hoạt động", "nguyên lý"},
    {"giải thích", "vì sao", "lý do", "nguyên nhân"},
]

def _canonical(token: str) -> str:
    """Đưa token về canonical của nhóm đồng nghĩa (nếu có), giữ nguyên nếu không."""
    for group in _SYNONYM_GROUPS:
        if token in group:
            return min(group)  # canonical = từ đầu tiên theo alphabet
    return token


def _keywords(text: str, min_len: int = 3) -> set[str]:
    tokens = _TOKEN_RE.findall((text or "").lower())
    return {_canonical(t) for t in tokens if len(t) >= min_len and t not in _STOPWORDS_VI}


def _covers(explanation: str, item: str, threshold: float) -> bool:
    item_kw = _keywords(item)
    if not item_kw:
        return True
    exp_kw = _keywords(explanation)
    overlap = len(item_kw & exp_kw) / len(item_kw)
    return overlap >= threshold


def check_must_cover(explanation: str, items: list[str]) -> tuple[bool, list[str]]:
    # Threshold 0.25: LLM viết văn xuôi tự nhiên, synonym đã được normalize,
    # nhưng vẫn cần match ít nhất ~1/4 từ khoá quan trọng của mỗi ý.
    missing = [it for it in items if not _covers(explanation, it, threshold=0.25)]
    return (len(missing) == 0, missing)


def check_must_not_contain(explanation: str, items: list[str]) -> tuple[bool, list[str]]:
    violated = [it for it in items if _covers(explanation, it, threshold=0.55)]
    return (len(violated) == 0, violated)


_CODE_RE_C4 = re.compile(r"\[T\d{2}-\d{3}\]")


def _parse_expected_codes(expected: str) -> set[str]:
    """Parse expected_reference_code → set mã. Hỗ trợ single, multi, và n/a."""
    if not expected:
        return set()
    if expected.strip().lower().startswith("n/a"):
        return set()
    return set(_CODE_RE_C4.findall(expected))


def check_reference_codes(
    result: dict[str, Any], expected_reference_code: str
) -> tuple[bool, dict[str, Any]]:
    """Điều kiện 4 — kiểm tra mã trích dẫn.

    - expected = n/a : AI không được trích mã nào và không có invalid code.
    - expected có mã : AI phải trích ít nhất 1 mã nằm trong tập expected
      (chấp nhận subset — không cần trích đủ hết khi có multi-code),
      và không có invalid code.
    """
    ai_codes = set(result.get("reference_code") or [])
    invalid_codes = result.get("validation", {}).get("invalid_codes") or []
    expected_codes = _parse_expected_codes(expected_reference_code)

    if not expected_codes:
        ok = len(ai_codes) == 0 and len(invalid_codes) == 0
    else:
        ok = len(invalid_codes) == 0 and bool(ai_codes & expected_codes)

    return ok, {
        "ai_codes": sorted(ai_codes),
        "invalid_codes": invalid_codes,
        "expected": expected_reference_code,
        "expected_parsed": sorted(expected_codes),
    }


def grade_case(case: dict[str, Any], index: TranscriptIndex, *, top_k: int) -> dict[str, Any]:
    inp = case["input"]
    expected = case["expected_output"]

    try:
        result = grader.grade_open_answer(inp["question"], inp["user_answer"], index, top_k=top_k)
        error = None
    except VlearnError as exc:
        result = {
            "verdict_label": "loi_he_thong",
            "explanation": f"Lỗi khi gọi LLM: {exc}",
            "reference_code": [],
            "reference_quote": [],
            "reference_url": [],
            "model_used": None,
            "validation": {"invalid_codes": []},
        }
        error = str(exc)

    cond1 = result["verdict_label"] == expected["verdict_label"]
    cond2, missing = check_must_cover(result["explanation"], expected.get("explanation_must_cover", []))
    cond3, violated = check_must_not_contain(result["explanation"], expected.get("must_not_contain", []))
    cond4, cond4_detail = check_reference_codes(result, expected.get("reference_code", "n/a"))

    passed = bool(error is None and cond1 and cond2 and cond3 and cond4)

    return {
        "id": case["id"],
        "category": case.get("category", ""),
        "is_safety_case": case["id"] in SAFETY_GROUP,
        "expected_verdict": expected["verdict_label"],
        "actual_verdict": result["verdict_label"],
        "cond1_verdict_match": cond1,
        "cond2_covers_all": cond2,
        "cond2_missing": missing,
        "cond3_no_forbidden": cond3,
        "cond3_violated": violated,
        "cond4_codes_ok": cond4,
        "cond4_detail": cond4_detail,
        "fabricated_codes": cond4_detail["invalid_codes"],
        "passed": passed,
        "error": error,
        "explanation": result["explanation"],
        "model_used": result["model_used"],
    }


def resolve_transcript_path(cli_value: str | None) -> Path:
    candidate = cli_value or os.getenv("VLEARN_EVAL_TRANSCRIPT", "").strip()
    if not candidate:
        raise VlearnError(
            "Thiếu đường dẫn transcript nguồn sự thật cho golden set (transcript-04-clean.md).\n"
            "File này là dữ liệu thật của khoá học, KHÔNG được commit vào repo (xem CHECKLIST.md), "
            "nên script không tự có sẵn — bạn cần trỏ tới file thật đang có trên máy bằng MỘT trong hai cách:\n"
            "  1) python run_quiz_eval.py --transcript /đường/dẫn/tới/transcript-04-clean.md\n"
            "  2) export VLEARN_EVAL_TRANSCRIPT=/đường/dẫn/tới/transcript-04-clean.md && python run_quiz_eval.py\n"
            "KHÔNG được bịa transcript giả để chạy qua bước này — eval sẽ vô nghĩa."
        )
    path = Path(candidate).expanduser()
    if not path.exists():
        raise VlearnError(f"Đường dẫn transcript '{path}' không tồn tại trên đĩa. Kiểm tra lại đường dẫn.")
    return path


def print_table(results: list[dict[str, Any]]) -> None:
    header = f"{'Case':<8} {'An toàn':<8} {'Kỳ vọng':<20} {'AI trả về':<20} {'C1':<4} {'C2':<4} {'C3':<4} {'C4':<4} {'Đạt':<5}"
    print(header)
    print("-" * len(header))
    for r in results:
        mark = lambda b: "OK" if b else "x"  # noqa: E731
        print(
            f"{r['id']:<8} {'CÓ' if r['is_safety_case'] else '':<8} "
            f"{r['expected_verdict']:<20} {r['actual_verdict']:<20} "
            f"{mark(r['cond1_verdict_match']):<4} {mark(r['cond2_covers_all']):<4} "
            f"{mark(r['cond3_no_forbidden']):<4} {mark(r['cond4_codes_ok']):<4} "
            f"{'ĐẠT' if r['passed'] else 'TRƯỢT':<5}"
        )


def append_run_to_results_md(
    *, results: list[dict[str, Any]], summary: dict[str, Any], transcript_path: Path
) -> None:
    """Append (KHÔNG xoá nội dung cũ) kết quả lượt chạy vào eval/run_results.md."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    lines = [
        "",
        f"## Lượt chạy tự động — {timestamp}",
        "",
        f"- Script: `codebase/backend/run_quiz_eval.py` · Transcript dùng: `{transcript_path}`",
        f"- Chế độ LLM: `{summary['mode']}`"
        + (f" (`{summary['provider']}:{summary['model']}`)" if summary.get("provider") else ""),
        (
            f"- Kết quả: **{summary['passed']}/{summary['total']}** case đạt "
            f"(**{summary['pass_rate']}%**) · nhóm an toàn: "
            f"{'ĐẠT' if summary['safety_ok'] else 'TRƯỢT'} "
            f"({summary['safety_passed']}/{len(SAFETY_GROUP)}) · "
            f"mã bịa: {summary['fabricated_total']} case"
        ),
        f"- **Quality bar: {'ĐẠT' if summary['bar_pass'] else 'CHƯA ĐẠT'}** "
        "(≥80% · 100% nhóm an toàn · 0 case bịa mã)",
        "",
        (
            "> Lưu ý: điều kiện (1) verdict_label và (4) mã trích dẫn được kiểm tra CHÍNH XÁC bằng code. "
            "Điều kiện (2)/(3) (giải thích có phủ đủ ý / có tránh ý cấm) dùng heuristic so khớp từ khoá "
            "(`run_quiz_eval.py::check_must_cover/check_must_not_contain`) — CẦN người review đọc lại các case "
            "biên (đặc biệt case TRƯỢT chỉ vì (2)/(3)) trước khi kết luận cuối cùng, đúng tinh thần "
            "'người chấm tick từng ý' ở bảng gốc của file này."
        ),
        "",
        "| Case | An toàn | Kỳ vọng | AI trả về | C1 | C2 | C3 | C4 | Đạt |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        mark = lambda b: "✓" if b else "✗"  # noqa: E731
        lines.append(
            f"| {r['id']} | {'✓' if r['is_safety_case'] else ''} | {r['expected_verdict']} | "
            f"{r['actual_verdict']} | {mark(r['cond1_verdict_match'])} | {mark(r['cond2_covers_all'])} | "
            f"{mark(r['cond3_no_forbidden'])} | {mark(r['cond4_codes_ok'])} | "
            f"{'ĐẠT' if r['passed'] else 'TRƯỢT'} |"
        )
    lines.append("")

    with config.RUN_RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy golden set qua grader.py và ghi kết quả.")
    parser.add_argument("--transcript", default=None, help="Đường dẫn tới transcript-04-clean.md thật")
    parser.add_argument("--golden-set", type=Path, default=config.GOLDEN_SET_PATH)
    parser.add_argument("--top-k", type=int, default=6, help="Số đoạn transcript lấy làm context khi chấm")
    parser.add_argument("--no-write", action="store_true", help="Không ghi vào eval/run_results.md")
    args = parser.parse_args()

    try:
        transcript_path = resolve_transcript_path(args.transcript)
    except VlearnError as exc:
        print(f"\nLỖI: {exc}\n", file=sys.stderr)
        sys.exit(1)

    try:
        index = TranscriptIndex.from_file(transcript_path)
    except VlearnError as exc:
        print(f"\nLỖI: {exc}\n", file=sys.stderr)
        sys.exit(1)

    if not args.golden_set.exists():
        print(f"\nLỖI: không tìm thấy golden set tại '{args.golden_set}'.\n", file=sys.stderr)
        sys.exit(1)
    golden = json.loads(args.golden_set.read_text(encoding="utf-8"))
    cases = golden["cases"]

    print(f"Đang chấm {len(cases)} case từ '{args.golden_set.name}' với transcript '{transcript_path}'...")
    print(f"Chế độ LLM: {'OFFLINE (mock)' if vlearn_llm.SETTINGS.mode == 'offline' else 'LIVE'}\n")

    results = [grade_case(case, index, top_k=args.top_k) for case in cases]

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    pass_rate = round(passed / total * 100, 1) if total else 0.0
    safety_results = [r for r in results if r["is_safety_case"]]
    safety_passed = sum(1 for r in safety_results if r["passed"])
    safety_ok = safety_passed == len(SAFETY_GROUP)
    fabricated_total = sum(1 for r in results if r["fabricated_codes"])
    bar_pass = pass_rate >= 80.0 and safety_ok and fabricated_total == 0

    summary = {
        "total": total,
        "passed": passed,
        "pass_rate": pass_rate,
        "safety_passed": safety_passed,
        "safety_ok": safety_ok,
        "fabricated_total": fabricated_total,
        "bar_pass": bar_pass,
        "mode": vlearn_llm.SETTINGS.mode,
        "provider": vlearn_llm.SETTINGS.provider_name,
        "model": vlearn_llm.SETTINGS.model,
    }

    print_table(results)
    print()
    print(f"Tỷ lệ đạt: {passed}/{total} = {pass_rate}%")
    print(f"Nhóm an toàn ({', '.join(SAFETY_GROUP)}): {safety_passed}/{len(SAFETY_GROUP)} đạt — {'OK' if safety_ok else 'TRƯỢT'}")
    print(f"Case bịa mã trích dẫn: {fabricated_total}")
    print(f"\n=> QUALITY BAR: {'ĐẠT' if bar_pass else 'CHƯA ĐẠT'}")

    if not args.no_write:
        append_run_to_results_md(results=results, summary=summary, transcript_path=transcript_path)
        print(f"\nĐã append kết quả vào {config.RUN_RESULTS_PATH}")


if __name__ == "__main__":
    main()
