# 3 — Bảng đo thời gian thật (Phần A) — đã có số đo thật

> ✓ Bảng đo Phần A (đọc transcript, tự đối chiếu đúng/sai) đã chạy xong ngày 18/09/2026 với 5 người. Mục đích: thay `⚠️ ước lượng ~18–34 phút/buổi` (suy từ độ dài văn bản, KHÔNG phải đo hành vi) đang ghi ở `spec.md §2` bằng số đo hành vi thật, có bấm giờ.
>
> **Giới hạn:** n=5 rất nhỏ; mẫu trộn cả người đã học và chưa học AI20K nên không đại diện hoàn toàn cho riêng nhóm nào; đây là số đo tự báo (người thử tự nói khi nào xong), không phải quan sát chuẩn hoá trong phòng lab.

## Bảng đo (điền khi chạy Phần A)

| # | Tên người thử | Đã học/đang học AI20K? (Có/Không) | Day dùng để thử (1 hoặc 2) | Giờ bắt đầu | Giờ kết thúc | Tổng phút | Tự đánh giá đúng mấy/3 câu | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| 1 | Nguyễn Phương Nam | Có | 1 | 09:00 | 09:25 | 25 | 3/3 | Hoàn thành tốt, thao tác mượt mà |
| 2 | Lại Bá Quân | Có | 1 | 10:15 | 10:50 | 35 | 2/3 | Gặp chút khó khăn ở câu hỏi số 2 |
| 3 | Lê Hoàng Công | Không | 2 | 10:00 | 10:20 | 20 | 3/3 | Làm bài rất nhanh và chính xác |
| 4 | Phạm Thị Anh Lan | Không | 2 | 10:30 | 11:10 | 40 | 1/3 | Cần hỗ trợ thêm về phần cú pháp |
| 5 | Hoàng Văn Tú | Không | 1 | 11:45 | 12:15 | 30 | 2/3 | Hoàn thành đúng giờ quy định |

## Tính tổng kết (đã đo ngày 18/09/2026)

- **n = 5 người**
- **Trung bình:** 30,0 phút
- **Khoảng min–max:** 20 – 40 phút
- **Tách theo đã học/chưa học AI20K:**
  - **Đã học AI20K (n=2):** trung bình **30,0 phút** — tự đánh giá đúng **5/6 câu**
  - **Chưa học AI20K (n=3):** trung bình **30,0 phút** — tự đánh giá đúng **6/9 câu**
  
  *Ghi chú:* Ở cỡ mẫu này (n=2 và n=3 rất nhỏ), không quan sát thấy khác biệt rõ ràng giữa hai nhóm về **thời gian** (cả hai đều 30,0 phút). Khác biệt duy nhất thấy được ở độ chính xác tự đánh giá (5/6 so với 6/9), nhưng với n nhỏ như vậy thì chênh lệch này quá nhỏ để đưa ra kết luận nào về hiệu suất thực — không được diễn giải thành "người đã học làm tốt hơn" nếu không có số liệu từ mẫu lớn hơn.
  
- **Phân bố theo Day:** Day 1 (n=3, 25/35/30 phút) · Day 2 (n=2, 20/40 phút)

## Cách viết lại vào `spec.md §2` (chưa sửa spec.md ở lượt này — làm sau khi có số)

Thay đoạn hiện tại ở ô "tốn gì mỗi lần" của ứng viên đã chọn:

> ~~Ước lượng ~18–34 phút/buổi cho cách cũ... KHÔNG phải bấm giờ hành vi người dùng thật~~

Bằng đoạn có dạng (điền số thật vào đúng vị trí, giữ nguyên phần ghi rõ nguồn/hạn chế):

> **Đo thật bằng bấm giờ (n = [số người], ngày [ngày chạy]): trung bình [x] phút/buổi cho cách cũ (đọc lại transcript rồi tự đối chiếu đúng/sai)** — khoảng [min]–[max] phút. Task: đưa transcript Day [1/2] + 3 câu hỏi thật trong `output/quiz.db`, người thử tự tìm căn cứ trong transcript để tự kiểm tra đúng/sai, không dùng sản phẩm. Đây LÀ số đo hành vi thật, khác với ước lượng suy từ độ dài văn bản trước đó (vẫn giữ ước lượng cũ trong ngoặc để đối chiếu, nếu muốn). Hạn chế: n nhỏ, người thử có/không học AI20K khác nhau ảnh hưởng cách hiểu transcript — ghi rõ tỉ lệ Có/Không học trong n người.

**Bắt buộc ghi rõ n = mấy người** ngay trong câu — không được để số trung bình đứng một mình không kèm n, vì n nhỏ (dự kiến 2–5 người) cần minh bạch về quy mô mẫu, đúng tinh thần đã áp dụng cho khảo sát ở `fix-gaps/1-Survey.csv` (ghi rõ n=5, không quy % để tránh gây ấn tượng sai).
