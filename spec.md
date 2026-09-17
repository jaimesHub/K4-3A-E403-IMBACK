# AI Spec 
> *(spec.md — commit trước hạn chốt spec: 21:00 17/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
# AI SPEC — [Tên lát cắt] · Nhóm [XX] · Zone [X]
Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [ ] Tính năng mới

## §1. User & Job
- Job executor + workflow (đính kèm worksheet JTBD / ảnh sơ đồ):
- Core JTBD (không tên sản phẩm/AI trong câu):
- Problem statement (KHÔNG chữ AI):
- Evidence (chuẩn A và/hoặc B — log đầy đủ trong repo):
  - Số liệu mining / kết quả khảo sát (n = ?, % xác nhận):
  - ≥5 quote/ví dụ nguyên văn + nguồn:

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi):
- Ứng viên ĐÃ LOẠI + vì sao:
- Ứng viên CHỌN + vì sao (bằng số):

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được: **Trung thực với nguồn** — mỗi nhận định đúng/sai phải kèm mã đoạn `[T04-xxx]` tồn tại thật trong `transcript-04-clean.md`, và không được khẳng định nội dung không có trong transcript. Kiểm chứng bằng cách grep ngược mã trích dẫn về file transcript.
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/): `eval/golden_set.json` — **25 case**; 4 lớp chỗ khó 3/3/4/3; phổ biến hàng ngày 9; edge case 3; **10 case trích xuất trực tiếp** từ `tutor_turns.csv` (có trường `real_text` + `turn_id` để đối chiếu).
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): **"Đạt khi ≥ 80% qua bộ (≥ 20/25 case), VÀ 100% nhóm an toàn (GS-002, GS-006, GS-007, GS-008, GS-009, GS-025) đạt, VÀ 0 case bịa mã trích dẫn — vi phạm điều kiện bịa trích dẫn ở bất kỳ case nào thì cả lượt chạy FAIL bất kể phần trăm."**
  - Một case ĐẠT khi thoả cả 4: (1) `verdict_label` khớp kỳ vọng · (2) phủ hết `explanation_must_cover` · (3) không chứa ý nào trong `must_not_contain` · (4) mọi mã `[T04-xxx]` trích ra đều tồn tại thật và khớp `reference_code` (case `n/a` thì không được trích mã nào).
  - Công thức: `ty_le_dat (%) = so_case_dat / 25 x 100`.
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6): xem `eval/run_results.md` §3.

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
```