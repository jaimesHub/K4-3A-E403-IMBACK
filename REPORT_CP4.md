# Báo cáo CP4 — Chốt spec.md

| Metadata | Chi tiết |
|---|---|
| **Nhóm** | I'M BACK |
| **Lớp / Phòng** | 3A / E403 |
| **Ngày chốt** | 17/9/2026 |
| **Branch** | `khanhdq/cp4` |
| **Commit chốt spec CP4** | `1b63b13` + `48539ca` (branch `khanhdq/cp4`) |
| **Commit chốt chuẩn "đạt"** | `687c8b4` (15:48:53) — đưa `eval/cp3_benchmark.py` + `eval/cp3_testset.json` vào repo |
| **Commit chạy kết quả LIVE** | `a2d829e` (16:03:55) — sau khi chốt chuẩn 15 phút |

---

## CP4 yêu cầu gì

Theo handbook trang 06:
- **Chốt chuẩn "đạt" TRƯỚC khi biết kết quả** — đảm bảo chuẩn không bị điều chỉnh dễ dàng khi thấy kết quả thực tế.
- **Nộp `spec.md` đã chốt** — trong đó nhóm tự chốt chuẩn "đạt" và khai rõ phần nào chưa làm xong.
- **Không sửa chuẩn "đạt" sau mốc này** — mốc CP4 là "bước ngoặt" của chuẩn kiểm chứng.
- **Nguyên tắc khai thiếu:** *"Khai thiếu không bị trừ điểm. Giấu mới bị."*

---

## Câu hỏi 1: Chuẩn "đạt" của nhóm

Nhóm chốt chuẩn ở **hai tầng khác nhau**, phải trình bày tách bạch vì đo trên bộ dữ liệu khác nhau.

### Tầng 1 (Chính thức): Golden Set 25 case

**Nguồn:** `eval/golden_set.json` — 25 case chọn lọc gồm 4 lớp chỗ khó (3/3/4/3), phổ biến hàng ngày (9 case), edge case (3 case), 10 case trích trực tiếp từ `tutor_turns.csv`.

**Chuẩn ĐẠT khi thoả CẢ BA điều kiện:**

1. **≥ 80% qua bộ:** ≥ 20/25 case đạt
2. **100% nhóm an toàn:** Các case GS-002, GS-006, GS-007, GS-008, GS-009, GS-025 phải tất cả đạt (6/6)
3. **0 case bịa mã trích dẫn:** Nếu phát hiện 1 case nào bịa mã `[T04-xxx]`, cả lượt chạy FAIL bất kể phần trăm

**Một case ĐẠT khi thoả cả 4 tiêu chí:**
- (1) `verdict_label` khớp `expected_verdict`
- (2) `explanation` phủ hết tất cả ý trong `explanation_must_cover`
- (3) `explanation` không chứa bất kỳ ý nào trong `must_not_contain`
- (4) Mọi mã `[T04-xxx]` trích ra đều tồn tại thật trong `transcript-04-clean.md` và khớp `reference_code` (case `n/a` thì không được trích mã nào)

**Công thức:** `ty_le_dat (%) = so_case_dat / 25 × 100`

**Trạng thái hiện tại:** ⚠️ **Chưa chạy được lần nào** — thiếu file `transcript-04-clean.md`.

---

### Tầng 2 (Đo tại CP3): Testset 24 case

**Nguồn:** `eval/cp3_testset.json` — 24 case từ các câu hỏi thật đang có trong `output/quiz.db` (Day 1 + Day 2), chạy qua `eval/cp3_benchmark.py` gọi API thật.

**Chuẩn ĐẠT khi thoả CẢ HAI điều kiện:**
- (1) `verdict_label` khớp `expected_verdict`
- (2) Mọi mã `[Txx-NNN]` trả ra đều có thật trong transcript (field `validation.invalid_codes` rỗng)

**Kết quả thật đã đo:**
- **Chế độ:** LIVE, `provider=openai`, `model=gpt-4o-mini`
- **Số case:** 21/24 đạt (**87.5%**)
- **Chi tiết:** 21 case trả đúng có dẫn nguồn, 3 case sai hoặc bịa
- **Độ tin cậy:** Chạy **2 lượt tách biệt** độc lập → kết quả **trùng khớp** (cả 2 lượt 21/24)
- **Bịa mã:** 0 case bịa mã trích dẫn ở cả 2 lượt
- **Ghi chép:** Chi tiết trong `eval/EVAL_REPORT_v1.md` và `eval/run_results.md`

**⚠️ Cảnh báo bắt buộc ghi trong báo cáo:**

> **87.5% là kết quả của bộ CP3 (24 case, Day 1–2), KHÔNG phải golden set (25 case, Day 4).**
>
> Hai bộ đo dùng transcript khác nhau, quy mô khác nhau, và tiêu chí ĐẠT cũng khác nhau:
> - CP3 testset: 2 điều kiện (verdict + không bịa mã)
> - Golden set: 4 điều kiện (verdict + phủ must_cover + không chứa must_not_contain + không bịa mã)
>
> **Chuẩn "đạt" chính thức ở tầng 1 hiện CHƯA CÓ SỐ vì golden set chưa chạy được lần nào.**

---

## Câu hỏi 2: Phần chưa làm xong

Nhóm khai rõ 6 mục chưa hoàn thành (đúng 6 mục, không thêm, không bớt):

| # | Mục | Chưa có gì | Ảnh hưởng điểm |
|---|---|---|---|
| 1 | §1 Evidence | Không có khảo sát/mining thật, không có log phỏng vấn, 0/5 quote nguyên văn + nguồn, không có n = ? hay % xác nhận vấn đề có thật | R1 · 15đ |
| 2 | §2 Impact | Có 3 ứng viên nhưng không có số thật (bao nhiêu người, tần suất, tốn gì mỗi lần); "ứng viên CHỌN vì sao bằng số" chưa trả lời được (thiếu số liệu từ mục 1) | R1 · 15đ |
| 3 | §7 Golden set | Bộ 25 case chưa chạy được lần nào — **thiếu đúng một file:** `transcript-04-clean.md`. Script sẵn sàng: `codebase/backend/run_quiz_eval.py --transcript <đường dẫn>` | R4 · 15đ |
| 4 | §8 Phân công | 4 thành viên thật nhưng vai trò (spec/evidence/prompt/code/demo) cả 4 người đều để **trống** — cũng trống luôn trong `TEAMMATES.md` | R7 + trình bày CP6 |
| 5 | §8 Willing users | Chưa có ai — không có thư mục `validation/`, không có `reflection/`. **Đây là R6 (8đ) làm ở CP5**, yêu cầu **5 người ngoài nhóm** dùng thử, trong đó **2 người phải đã khai từ CP1** | R6 · 8đ (làm ở CP5) |
| 6 | Multi-prototype | Không làm — chỉ có một phương án lát cắt duy nhất (quiz tự luận + MCQ chấm theo transcript), không có phương án thứ hai so sánh | Bonus · không mất điểm |

---

## Thứ tự ưu tiên phải làm

Theo handbook trang 06, 08, 09:

1. **🔴 Gấp nhất: Mục 5 (Willing users)** — Handbook trang 09 yêu cầu R6 phải có **5 người ngoài nhóm** dùng thử, trong đó **2 người bắt buộc đã khai từ CP1**. Nếu không làm, trần điểm chỉ còn **92/100** (mất 8đ R6). **Hành động ngay:** Xác nhận nhóm đã khai willing users từ CP1 chưa; nếu chưa, phải tìm và chốt ≥2 người sẵn sàng dùng thử trước CP5.

2. **🟠 Kế đến: Mục 3 (Golden set)** — Chỉ cần xin được file `transcript-04-clean.md` (do người khác giữ/cấp), chạy script eval, và điền bảng ở `eval/run_results.md §3`. Là 15 điểm đang bỏ trống vì thiếu đúng một file.

3. **🟡 Kế: Mục 1 & 2 (Evidence & Impact)** — Nặng nhất (15+15=30đ) và không ai làm hộ được. Cần có người thật đi khảo sát/mining, lấy quote nguyên văn, tính % xác nhận. Sau đó mới điền bảng impact bằng số.

4. **🟢 Sau cùng: Mục 4 (Phân công)** — Cả nhóm họp, điền vai trò cụ thể cho từng người (spec/evidence/prompt/code/demo) ở cả `spec.md` và `TEAMMATES.md`, rồi trình bày kế hoạch ở CP6.

---

## Bằng chứng chốt chuẩn trước khi biết kết quả

**Timeline chốt:**
- **15:48:53** — Commit `687c8b4`: Chốt chuẩn "đạt" (quality bar golden set ≥80% + 100% nhóm an toàn + 0 bịa mã)
- **16:03:55** — Commit `a2d829e`: Chạy lượt LIVE đầu tiên qua LLM thật
- **Chênh lệch:** 15 phút — chuẩn được chốt TRƯỚC khi lấy kết quả thực tế ✓

Đúng tinh thần CP4 / handbook trang 06: *"Khai thiếu không bị trừ điểm. Giấu mới bị."*

---

## Ghi chú tính trung thực

Theo handbook trang 08: *"Kết quả đo ghi nhận trung thực — kể cả khi không đạt mục tiêu nhóm tự đặt — vẫn được tính đủ điểm. Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính."*

Sáu mục chưa làm ở trên **đã khai thẳng trong `spec.md`** ngay tại các mục tương ứng (đánh dấu khối `⚠️ CHƯA LÀM XONG`). Không có số liệu hoặc quote nào trong `spec.md` là bịa; chỗ nào còn thiếu dữ liệu thật thì để trống và nói rõ cần gì.

---

## Tham chiếu file liên quan

| File | Mục đích |
|---|---|
| `spec.md` | Spec 8 phần chốt tại CP4 — bao gồm cả phần Evidence/Impact/Willing users/Phân công chưa làm xong |
| `eval/EVAL_REPORT_v1.md` | Phân tích chi tiết 3 case trượt CP3, trung thực không bịa |
| `eval/run_results.md` | Bảng tóm tắt kết quả từng lượt chạy (OFFLINE 75%, LIVE 87.5%) |
| `eval/golden_set.json` | Golden set 25 case — chưa chạy được lần nào |
| `eval/cp3_testset.json` | CP3 testset 24 case — kết quả thật 21/24 (87.5%) |
| `CP3.md` | Báo cáo CP3 (nộp trước CP4) |
| `RUNBOOK.md` | Hướng dẫn tái lập pipeline an toàn |
| `TEAMMATES.md` | Danh sách thành viên + vai trò (hiện để trống vai trò) |

---

*Báo cáo này được tạo trên branch `khanhdq/cp4` vào ngày 17/9/2026.*
