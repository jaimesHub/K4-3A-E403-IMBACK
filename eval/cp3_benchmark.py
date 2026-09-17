"""CP3 — "số đo": thử bao nhiêu câu, đúng bao nhiêu câu có dẫn nguồn.

Chạy toàn bộ `eval/cp3_testset.json` (24 case) qua HTTP API THẬT của backend
(`POST /api/answer`, `GET /api/health`) — KHÔNG import thẳng module Python,
để phép đo phản ánh đúng cái người dùng thật sẽ trải nghiệm qua UI.

Cách dùng (backend phải đang chạy sẵn):
    cd codebase/backend && python3 -m uvicorn api:app --port 8000 &
    cd ../..
    python3 eval/cp3_benchmark.py
    # hoặc trỏ base URL khác:
    python3 eval/cp3_benchmark.py --base-url http://127.0.0.1:8000

Định nghĩa ĐẠT của MỘT case (ghi rõ ở đây, không mơ hồ):
    Một câu tính là ĐẠT khi thoả CẢ HAI điều kiện:
      (1) `verdict_label` API trả về khớp với `expected_verdict` trong testset.
      (2) Mọi mã trích dẫn `[Txx-NNN]` API trả ra đều tồn tại thật trong
          transcript — tức `validation.invalid_codes` rỗng.

Số đo in ra đúng định dạng handbook yêu cầu:
    "Thử N câu, X câu trả đúng có dẫn nguồn, Y câu sai hoặc bịa"
    (X = số case ĐẠT, Y = N - X = số case verdict sai HOẶC có mã bịa)

QUAN TRỌNG — trung thực với số liệu: script này KHÔNG tự bịa số, không tự
đoán live/offline. Chế độ chạy (`live`/`offline`) được đọc thật từ
`GET /api/health` ngay tại thời điểm chạy và được ghi rõ vào output + vào
`eval/run_results.md`. Nếu server đang OFFLINE (mock, chưa có API key), kết
quả vẫn được in và ghi lại đầy đủ, nhưng PHẢI được hiểu là số của chế độ mock —
KHÔNG phải số nộp CP3 (CP3 đòi hỏi ≥1 lời gọi AI chạy thật).
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTSET_PATH = REPO_ROOT / "eval" / "cp3_testset.json"
RUN_RESULTS_PATH = REPO_ROOT / "eval" / "run_results.md"

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


class ApiError(RuntimeError):
    pass


def _http_json(url: str, *, method: str = "GET", body: dict[str, Any] | None = None, timeout: float = 30.0) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
            msg = payload.get("error") or payload.get("detail") or raw
        except json.JSONDecodeError:
            msg = raw
        raise ApiError(f"HTTP {exc.code}: {msg}") from exc
    except urllib.error.URLError as exc:
        raise ApiError(
            f"Không kết nối được tới '{url}': {exc.reason}. "
            "Kiểm tra backend đã chạy chưa: cd codebase/backend && python3 -m uvicorn api:app --port 8000"
        ) from exc


def get_health(base_url: str) -> dict[str, Any]:
    return _http_json(f"{base_url}/api/health")


def post_answer(base_url: str, question_id: str, user_answer: str) -> dict[str, Any]:
    return _http_json(
        f"{base_url}/api/answer",
        method="POST",
        body={"question_id": question_id, "user_answer": user_answer},
    )


def grade_case(base_url: str, case: dict[str, Any]) -> dict[str, Any]:
    try:
        result = post_answer(base_url, case["question_id"], case["user_answer"])
        error = None
    except ApiError as exc:
        result = {
            "verdict_label": "loi_goi_api",
            "explanation": str(exc),
            "reference_code": [],
            "validation": {"invalid_codes": []},
            "model_used": None,
        }
        error = str(exc)

    actual_verdict = result.get("verdict_label")
    invalid_codes = (result.get("validation") or {}).get("invalid_codes") or []
    cond1_verdict_match = error is None and actual_verdict == case["expected_verdict"]
    cond2_no_fabricated_codes = len(invalid_codes) == 0
    passed = bool(cond1_verdict_match and cond2_no_fabricated_codes)

    return {
        "id": case["id"],
        "group": case.get("group", ""),
        "qtype": case.get("qtype"),
        "day": case.get("day"),
        "question_id": case.get("question_id"),
        "reference_code": case.get("reference_code"),
        "user_answer": case.get("user_answer"),
        "expected_verdict": case["expected_verdict"],
        "actual_verdict": actual_verdict,
        "cond1_verdict_match": cond1_verdict_match,
        "cond2_no_fabricated_codes": cond2_no_fabricated_codes,
        "invalid_codes": invalid_codes,
        "passed": passed,
        "error": error,
        "explanation": result.get("explanation"),
        "reference_code_actual": result.get("reference_code"),
        "model_used": result.get("model_used"),
    }


def print_table(results: list[dict[str, Any]]) -> None:
    header = f"{'Case':<9} {'Nhóm':<24} {'Kỳ vọng':<20} {'AI trả về':<20} {'C1':<4} {'C2':<4} {'Đạt':<6}"
    print(header)
    print("-" * len(header))
    for r in results:
        mark = lambda b: "OK" if b else "x"  # noqa: E731
        print(
            f"{r['id']:<9} {r['group']:<24} {r['expected_verdict']:<20} "
            f"{str(r['actual_verdict']):<20} {mark(r['cond1_verdict_match']):<4} "
            f"{mark(r['cond2_no_fabricated_codes']):<4} {'ĐẠT' if r['passed'] else 'TRƯỢT':<6}"
        )
        if r["error"]:
            print(f"          lỗi gọi API: {r['error']}")
        if r["invalid_codes"]:
            print(f"          mã bịa phát hiện: {r['invalid_codes']}")


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    fabricated_total = sum(1 for r in results if r["invalid_codes"])
    text_only = [r for r in results if r["qtype"] == "text"]
    text_passed = sum(1 for r in text_only if r["passed"])
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total * 100, 1) if total else 0.0,
        "fabricated_total": fabricated_total,
        "text_total": len(text_only),
        "text_passed": text_passed,
    }


def append_run_to_results_md(*, results: list[dict[str, Any]], summary: dict[str, Any], health: dict[str, Any], base_url: str) -> None:
    """Append (KHÔNG xoá nội dung cũ) kết quả lượt chạy CP3 vào eval/run_results.md."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    mode = health.get("mode", "unknown")
    mode_label = "LIVE" if mode == "live" else "OFFLINE (MOCK)"

    lines = [
        "",
        "---",
        "",
        f"## CP3 — Số đo \"thử bao nhiêu, đúng bao nhiêu\" — {timestamp}",
        "",
    ]
    if mode != "live":
        lines += [
            "> ⚠️ **CHẾ ĐỘ OFFLINE (MOCK) — ĐÂY KHÔNG PHẢI SỐ NỘP CP3.**",
            "> `.env` chưa có API key nên toàn bộ chấm bài tự luận ở lượt chạy này dùng heuristic so khớp",
            "> từ khoá (`vlearn/grader.py::_mock_grade`), KHÔNG phải LLM thật. CP3 yêu cầu ≥1 lời gọi AI",
            "> chạy thật — con số dưới đây CHỈ để kiểm tra pipeline/testset chạy đúng end-to-end qua HTTP API,",
            "> KHÔNG được dùng để báo cáo độ chính xác AI cho CP3.",
            "",
        ]
    lines += [
        f"- Script: `eval/cp3_benchmark.py` · Testset: `eval/cp3_testset.json` ({summary['total']} case) · Base URL: `{base_url}`",
        f"- Chế độ AI lúc chạy (`GET /api/health`): **{mode_label}**"
        + (f" — provider=`{health.get('provider')}`, model=`{health.get('model')}`" if mode == "live" else ""),
        "",
        f"**Thử {summary['total']} câu, {summary['passed']} câu trả đúng có dẫn nguồn, {summary['failed']} câu sai hoặc bịa.**",
        "",
        (
            f"- Tỉ lệ đạt: {summary['pass_rate']}% ({summary['passed']}/{summary['total']})"
        ),
        f"- Trong đó nhóm câu tự luận có AI chấm thật (`qtype=text`): {summary['text_passed']}/{summary['text_total']} đạt",
        f"- Số case bị phát hiện mã trích dẫn bịa (`validation.invalid_codes` không rỗng): {summary['fabricated_total']}",
        "",
        (
            "> Định nghĩa ĐẠT: (1) `verdict_label` khớp `expected_verdict` trong testset, VÀ "
            "(2) không có mã `[Txx-NNN]` bịa (`validation.invalid_codes` rỗng). Xem chi tiết trong "
            "docstring đầu file `eval/cp3_benchmark.py`."
        ),
        "",
        "| Case | Nhóm | Kỳ vọng | AI trả về | C1 khớp verdict | C2 không bịa mã | Đạt |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        mark = lambda b: "✓" if b else "✗"  # noqa: E731
        lines.append(
            f"| {r['id']} | {r['group']} | {r['expected_verdict']} | {r['actual_verdict']} | "
            f"{mark(r['cond1_verdict_match'])} | {mark(r['cond2_no_fabricated_codes'])} | "
            f"{'ĐẠT' if r['passed'] else 'TRƯỢT'} |"
        )
    lines.append("")

    with RUN_RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy eval/cp3_testset.json qua HTTP API thật và ghi số đo CP3.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"URL backend đang chạy (mặc định {DEFAULT_BASE_URL})")
    parser.add_argument("--testset", type=Path, default=TESTSET_PATH)
    parser.add_argument("--no-write", action="store_true", help="Không ghi vào eval/run_results.md")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")

    try:
        health = get_health(base_url)
    except ApiError as exc:
        print(f"\nLỖI: {exc}\n", file=sys.stderr)
        sys.exit(1)

    if not args.testset.exists():
        print(f"\nLỖI: không tìm thấy testset tại '{args.testset}'.\n", file=sys.stderr)
        sys.exit(1)
    testset = json.loads(args.testset.read_text(encoding="utf-8"))
    cases = testset["cases"]

    mode = health.get("mode", "unknown")
    mode_label = "LIVE" if mode == "live" else "OFFLINE (mock)"
    print(f"Backend: {base_url} · Chế độ AI: {mode_label}", end="")
    if mode == "live":
        print(f" (provider={health.get('provider')}, model={health.get('model')})")
    else:
        print()
        print(
            "⚠ CẢNH BÁO: backend đang OFFLINE (mock) — kết quả dưới đây KHÔNG phải số nộp CP3. "
            "Điền API key vào codebase/backend/.env rồi khởi động lại server để chạy LIVE."
        )
    print(f"Đang gọi POST /api/answer thật cho {len(cases)} case từ '{args.testset.name}'...\n")

    results = [grade_case(base_url, case) for case in cases]
    summary = summarize(results)

    print_table(results)
    print()
    print(f"Thử {summary['total']} câu, {summary['passed']} câu trả đúng có dẫn nguồn, {summary['failed']} câu sai hoặc bịa.")
    print(f"Tỉ lệ đạt: {summary['pass_rate']}%")
    print(f"Riêng nhóm tự luận có AI chấm thật: {summary['text_passed']}/{summary['text_total']} đạt.")
    if summary["fabricated_total"]:
        print(f"⚠ Có {summary['fabricated_total']} case bị phát hiện mã trích dẫn bịa.")

    if not args.no_write:
        append_run_to_results_md(results=results, summary=summary, health=health, base_url=base_url)
        print(f"\nĐã append kết quả lượt chạy vào {RUN_RESULTS_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
