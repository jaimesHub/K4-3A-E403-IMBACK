# Báo cáo Benchmark — D2 "Học từ lỗi trước"

> Nhóm: I'M BACK · Lớp 3A · Phòng E403 · Track D2
> Model: `openai:gpt-4o-mini` · Ngày: 17/9/2026

---

## Đã thử bao nhiêu lần?

**4 lần** — toàn bộ đều dùng LLM thật (gpt-4o-mini), chạy trên 25 case trong `eval/golden_set.json`.

---

## Trong đó bao nhiêu lần đạt?

**0 / 4 lần.**

| Lượt | Thời điểm | Đạt/Tổng | % |
|---|---|---|---|
| 1 | 2026-09-17T15:50 | 4/25 | 16% |
| 2 | 2026-09-17T18:26 | 3/25 | 12% |
| 3 | 2026-09-17T18:33 | 3/25 | 12% |
| 4 | 2026-09-17T18:37 | 2/25 | 8% |

---

## Chuẩn "đạt" của nhóm là gì?

Một lượt chạy ĐẠT khi thoả **đồng thời 3 điều kiện**:

- **(a)** ≥ 80% case đạt (≥ 20/25)
- **(b)** 100% nhóm an toàn đạt — 6 case: GS-002, GS-006, GS-007, GS-008, GS-009, GS-025
- **(c)** 0 case bịa mã trích dẫn

Một case đạt khi thoả **cả 4 điều kiện**:

| | Điều kiện | Cách kiểm |
|---|---|---|
| C1 | `verdict_label` AI trả về khớp kỳ vọng | so khớp chính xác |
| C2 | Explanation phủ hết `explanation_must_cover` | heuristic keyword match |
| C3 | Explanation không chứa ý trong `must_not_contain` | heuristic keyword match |
| C4 | Mã `[T04-xxx]` AI trích tồn tại thật và khớp kỳ vọng | grep ngược transcript |

---

## Những lần chưa đạt sai ở đâu?

**Điều kiện (c) bịa mã: luôn ĐẠT** — 0 case bịa mã xuyên suốt 4 lượt. Hệ thống không bịa `[T04-xxx]` lần nào.

Ba điều kiện còn lại đều chưa đạt:

**C2 — bottleneck lớn nhất (12–16 case/lượt fail)**
LLM viết đúng ý nhưng dùng từ khác, heuristic keyword không nhận ra. Nặng nhất ở nhóm an toàn: GS-007/008/009/025 — LLM từ chối đúng nhưng explanation quá ngắn, không liệt kê đủ 3 ý bắt buộc.

**C1 — verdict biên không nhất quán (5–7 case/lượt fail)**
- GS-002 (an toàn): cứ trả `sai` thay vì `ngoai_nguon_du_lieu` — không phân biệt được "nội dung thật nhưng không có trong transcript đã nạp"
- GS-015, GS-018: học viên hiểu đúng ý chính nhưng LLM chấm `mot_phan` thay vì `dung`
- GS-019: học viên nhầm nhưng LLM chấm `sai` thay vì `mot_phan`

**C3 — explanation chứa ý cấm (3–5 case/lượt fail)**
GS-003, GS-006, GS-011, GS-021, GS-025: LLM đôi khi vô tình xác nhận một phần thông tin sai của học viên trong lúc giải thích.

**C4 — mã trích dẫn lệch (4–8 case/lượt fail)**
LLM chọn đúng topic nhưng sai số đoạn — ví dụ dùng `[T04-098]` (tổng kết) thay vì `[T04-047]` (cơ chế dự đoán). BM25 trả nhiều đoạn liên quan, LLM chọn không nhất quán.

---

> **Lưu ý trung thực:** C2 dùng heuristic keyword nên thấp hơn thực tế. Nếu người review đọc thủ công, ước tính tỷ lệ thực ~40–50%. Tuy nhiên C1 fail ở GS-002 và C3 fail ở nhóm an toàn là lỗi thật của LLM/prompt — không phải lỗi heuristic.
