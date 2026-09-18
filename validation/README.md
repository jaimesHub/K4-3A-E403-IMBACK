# validation/ — Đã chạy xong vòng dùng thử thật (Phần B, 5 người)

> ✓ **Đã chạy xong vòng dùng thử sản phẩm thật (Phần B) trên branch `khanhdq/cp5`, với 5 người dùng thử ngoài nhóm.** Bảng nhật ký dưới đây có tên người thử, task được giao, chỗ kẹt và quote nguyên văn — chép đúng lời nói, không diễn giải hay "làm đẹp" câu chữ, kể cả khi có lỗi chính tả. Vẫn còn một số điểm cần người chạy buổi thu dữ liệu xác nhận lại — xem các khối `⚠️` rải trong file (ngày tháng ghi trong bảng, và cột "Có làm Phần A" đối chiếu với danh sách tên khác ở `fix-gaps/3-BANG-DO-THOI-GIAN.md`).

Theo handbook trang 09 (R6, CP5 — 8 điểm), yêu cầu:

- **5 người dùng thử ngoài nhóm**, trong đó **2 người đã được khai từ CP1**.
- Mỗi người thử được giao một task cụ thể (ví dụ: upload transcript → generate quiz → trả lời 1 câu tự luận → đọc kết quả chấm).
- Ghi lại **bảng nhật ký**: ai thử, giao task gì, kẹt ở đâu, quote nguyên văn, quyết định của nhóm sau khi nghe.
- **Quote phải chép đúng nguyên văn**, kể cả khi người dùng viết sai chính tả hoặc nói lấp lửng — không được diễn giải lại hay "làm đẹp" câu nói.
- Từ những feedback này, chọn **≥1 thay đổi thật** để ghi vào `spec.md §9 Changelog` (trỏ rõ về feedback/case nào).

## Cách chạy buổi thu dữ liệu (hướng dẫn thao tác, mới thêm 18/9)

> Không sửa nội dung có sẵn dưới đây — chỉ thêm mục này để trỏ sang hướng dẫn thao tác cụ thể, và thêm 1 cột vào bảng nhật ký để ghi được cả kết quả Phần A (đo thời gian cách cũ) lẫn Phần B (dùng thử sản phẩm) trong cùng một buổi.

- **Hướng dẫn thao tác từng bước, kèm kịch bản nói với người thử và mốc thời gian cho mỗi bước:** `fix-gaps/3-HUONGDAN-THU-DU-LIEU.md`.
- **Bảng đo thời gian thật (Phần A — thay ước lượng 18–34 phút ở `spec.md §2`):** `fix-gaps/3-BANG-DO-THOI-GIAN.md`.
- Bảng nhật ký ngay dưới đây (Phần B) dùng để ghi kết quả dùng thử sản phẩm — đã thêm cột "Phần A?" để đánh dấu người thử nào cũng có làm Phần A (chi tiết thời gian nằm ở file riêng, không lặp lại ở đây).

## Trạng thái hiện tại

- Số người **đã thực sự dùng thử**: **5/5** (đã chạy xong vòng dùng thử — xem bảng nhật ký dưới)
- Số người **đã dùng thử, có nguồn gốc willing user từ CP1**: **2/2** (Nguyễn Phương Nam, Lại Bá Quân — điều kiện "≥2 người từ CP1" của R6 đã thoả, và cả 2 **đã thực sự dùng thử**, không chỉ "đã chốt sẵn sàng")
- **Điều kiện R6 (5 người ngoài nhóm, ≥2 người từ CP1) coi như đã đủ về số lượng và nguồn gốc** — xem bảng dưới và bảng nhật ký. **Cả 5 người đã thực sự dùng thử Phần B; 2/5 người (Nam, Quân) đã đánh dấu "Có" làm Phần A** — nhóm xác nhận lại danh sách tên và ngày khi có cơ hội.
- Thư mục này trước khi chạy buổi thu dữ liệu: **không tồn tại** trong repo.

## Danh sách 5 người dùng thử (Phần B)

> **Lưu ý đặt tên bảng:** đây không phải bảng "willing user" — willing user khai từ CP1 chỉ có **2 người** (Nguyễn Phương Nam, Lại Bá Quân, đánh dấu "Có" ở cột dưới). 3 người còn lại (Trần Minh Tuấn, Lê Hoàng Anh, Phạm Quỳnh Nga) là người dùng thử **tuyển thêm** cho đủ điều kiện R6 (5 người ngoài nhóm), **không phải** willing user đã khai từ CP1.

| #   | Tên               | Vai/quan hệ                         | Đã khai từ CP1 (willing user) |
| --- | ----------------- | ----------------------------------- | ------------------------------ |
| 1   | Nguyễn Phương Nam | Học viên cùng khoá K4               | **Có** — willing user từ CP1   |
| 2   | Lại Bá Quân       | Học viên cùng khoá K4               | **Có** — willing user từ CP1   |
| 3   | Trần Minh Tuấn    | Lập trình viên Backend (ngoài nhóm) | Không — tuyển thêm cho R6       |
| 4   | Lê Hoàng Anh      | Sinh viên CNTT năm cuối             | Không — tuyển thêm cho R6       |
| 5   | Phạm Quỳnh Nga    | Product Owner tập sự                | Không — tuyển thêm cho R6       |


**Ghi chú:** Đã đủ **5/5** người ngoài nhóm, trong đó **2/2** người có nguồn gốc willing user từ CP1 (Nam, Quân). Cả 5 người đều **đã thực sự dùng thử** (không còn ở trạng thái "mới chốt, chưa dùng thử" như bản trước) — quote nguyên văn và chỗ kẹt của từng người xem bảng nhật ký dưới.

## Bảng nhật ký (đã điền dữ liệu thật)

| #   | Tên người thử     | Đã khai từ CP1? | Ngày thử   | Có làm Phần A (bấm giờ)? — nếu có, xem `fix-gaps/3-BANG-DO-THOI-GIAN.md` ⚠️ *(tên không khớp — xem cảnh báo trên)* | Task được giao (Phần B)                               | Kẹt ở đâu (mô tả cụ thể)                                                                           | Quote nguyên văn (chép đúng, kể cả sai chính tả)                                                           | Quyết định của nhóm sau khi nghe                                                                                   |
| --- | ----------------- | --------------- | ---------- | ------------------------------------------------------------------------ | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1   | Nguyễn Phương Nam | Có              | 16/09/2026 | Có ⚠️                                                                    | Upload file transcript buổi học, tạo quiz và làm bài  | Upload định dang khác .pdf , thì lỗi. Sau khi giải thích thì mới biết app chỉ support .pdf         | *"Ơ sao không upload được định dạng .md nhỉ?"*                                                             | Cần bổ sung thêm hỗ trợ định dạng khác                                                                             |
| 2   | Lại Bá Quân       | Có              | 16/09/2026 | Có ⚠️                                                                    | Generate quiz từ transcript dài và nộp bài tự luận    | Chờ hệ thống gọi API generate quiz mất hơn 10s nhưng không có thanh loading bar báo trạng thái     | *"Đứng hình mất 5s, tưởng web chết r chứ ko thấy chạy j sất, bổ sung thanh loading đi ông ơi"*             | Bổ sung thanh tiến trình (progress bar/spinner) và dòng chữ "Đang tạo câu hỏi bằng AI..." khi hệ thống đang xử lý. |
| 3   | Trần Minh Tuấn    | Không           | 17/09/2026 | Không ⚠️                                                                    | Trả lời câu hỏi tự luận và xem kết quả AI chấm điểm   | Nhập xong câu trả lời, nhưng AI trả lời hơi chung chung, chưa cho ra câu trả lời rõ ràng, dễ hiểu  | *"Câu trả lơi có vẻ chưa được rõ ràng nhỉ , hơi chung chung ?"*                                            | Cần thay đổi cách AI đưa ra câu trả lời rõ ràng, cụ thể hơn                                                        |
| 4   | Lê Hoàng Anh      | Không           | 17/09/2026 | Không ⚠️                                                                    | Đọc phần kết quả chấm tự luận và feedback chi tiết    | Bối rối vì phần giải thích của AI dùng từ ngữ quá hàn lâm, khó hiểu ở mục đánh giá logic           | *"Đọc cái giải thích này lú thế nhờ, chữ nghĩa cứ hàn lâm sao ấy, ko hiểu nó trừ điểm mình vì thiếu ý gì"* | Viết lại prompt hướng dẫn AI trả về kết quả chấm ngắn gọn, trực diện, gạch đầu dòng rõ các ý thiếu.                |
| 5   | Phạm Quỳnh Nga    | Không           | 18/09/2026 ⚠️ | Không ⚠️                                                                | Thực hiện toàn bộ luồng từ Phần A đến Phần B liên tục | Quên mất tiêu chí chấm điểm tự luận khi đang gõ bài làm vì màn hình không hiển thị đề bài kèm theo | *"Làm đến câu tự luận xong quên bố nó đề hỏi cái j, lướt lên lướt xuống bực ghê"*                          | Thiết kế giao diện chia đôi màn hình (split-view) hoặc ghim đề bài/tiêu chí ở khung bên trái khi làm phần tự luận. |

> Ghi chú quote: mọi quote trên chép **đúng nguyên văn**, kể cả lỗi chính tả/viết tắt ("Câu trả lơi", "chạy j sất", "r", "bố nó") — không được sửa lại cho đúng ngữ pháp hay "làm đẹp" câu chữ, theo đúng yêu cầu handbook.

## 4 dòng tổng kết cuối bảng


| Mục                                    | Nội dung                                                                                                                                                |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chủ đề lặp nhiều nhất trong feedback   | Giao diện thiếu tính trực quan ở các trạng thái chờ (loading), câu trả lời của AI chưa rõ ràng                                                          |
| Sẽ sửa gì **trước** demo (ưu tiên ngay) | Thêm thanh loading state khi gọi API generate quiz (Case #2); làm rõ/cụ thể hơn câu trả lời của AI (Case #3); viết lại prompt chấm tự luận để giảm ngôn ngữ hàn lâm (Case #4); ghim đề bài/tiêu chí khi làm tự luận (Case #5). **Cả 4 mục đều mới ở mức ĐÃ QUYẾT ĐỊNH, CHƯA THỰC HIỆN** — xem trạng thái từng mục ở bảng Changelog ngay dưới. |
| Giữ nguyên gì và vì sao                | Giữ nguyên độ chính xác của core logic AI chấm bài tự luận vì người dùng đều đánh giá phần nhận xét khá sát thực tế dù đôi chỗ từ ngữ còn hơi dài dòng. |
| Gì để dành sau (không sửa ngay)        | Tính năng lưu lịch sử bài làm cá nhân vào tài khoản cloud và phân quyền nhóm (ngoài phạm vi demo CP5); hỗ trợ upload định dạng khác .pdf (Case #1, Nguyễn Phương Nam) — mức độ ưu tiên thấp hơn 4 mục ở dòng trên, chưa chốt thời điểm làm. |


## Thay đổi đã ghi vào Changelog (đối chiếu `spec.md §9`)

> **Ghi chú:** Các dòng dưới đây là thay đổi **ĐÃ QUYẾT ĐỊNH** từ feedback thật. Đã kiểm tra bằng `git status`: các file prompt chấm tự luận chưa hề bị sửa trong working tree — cột "Trạng thái" ghi rõ để không hiểu lầm là đã làm xong.

| Thời điểm dự kiến | Thay đổi                                                                                 | Feedback/case nào                    | Trạng thái |
| ----------------- | ------------------------------------------------------------------------------------------ | -------------------------------------- | ---------- |
| Sau demo 18/09/2026 | Bổ sung thanh tiến trình (progress bar/spinner) + dòng chữ "Đang tạo câu hỏi bằng AI..." khi generate quiz | Trỏ về Case #2 (Lại Bá Quân).          | **Đã quyết định — CHƯA THỰC HIỆN** (không thấy thay đổi tương ứng trong code) |
|Sau demo 18/09/2026 | Điều chỉnh cách AI trả lời/prompt chấm tự luận để câu trả lời rõ ràng, cụ thể hơn, tránh chung chung | Trỏ về Case #3 (Trần Minh Tuấn).       | **Đã quyết định — CHƯA THỰC HIỆN** |
| Sau demo 18/09/2026 | Tối ưu hóa prompt AI chấm tự luận (`codebase/backend/vlearn/prompts/grade_text.md`) để trả về kết quả dạng gạch đầu dòng ngắn gọn, dễ đọc, giảm ngôn ngữ hàn lâm | Trỏ về Case #4 (Lê Hoàng Anh).         | **Đã quyết định — CHƯA THỰC HIỆN** (đã kiểm tra `git status`: file prompt chưa bị sửa) |
| Sau demo 18/09/2026 | Thiết kế giao diện chia đôi màn hình (split-view) hoặc ghim đề bài/tiêu chí khi làm phần tự luận | Trỏ về Case #5 (Phạm Quỳnh Nga).       | **Đã quyết định — CHƯA THỰC HIỆN** |

> Case #1 (Nguyễn Phương Nam — hỗ trợ định dạng upload khác .pdf) **chưa được đưa vào Changelog ưu tiên** — xem dòng "Gì để dành sau" ở bảng 4 dòng tổng kết trên; đây cũng chỉ là quyết định, chưa thực hiện.

## Cách dùng file này

> Sau khi có thay đổi **thực sự được code**, nhớ cập nhật lại cột "Trạng thái" ở bảng trên thành "Đã thực hiện" và đồng bộ dòng tương ứng vào bảng Changelog ở `spec.md §9` — không được đổi trạng thái thành "đã thực hiện" trước khi code thật sự đổi.

1. Chốt danh sách 5 người dùng thử (2 người từ CP1) — đã xong, xem bảng "Danh sách 5 người dùng thử" ở trên.
2. Giao task cụ thể cho từng người, quan sát trực tiếp (không hỏi qua loa "thấy sao?") — đã làm, xem bảng nhật ký ở trên.
3. Chép quote nguyên văn ngay lúc nghe — không paraphrase, không "chỉnh cho mượt" — đã làm, xem cột Quote ở bảng nhật ký.
4. Điền bảng nhật ký + 4 dòng tổng kết ở trên — đã làm.
5. Chọn ≥1 thay đổi thật, cập nhật `spec.md §9` — đã chọn 4 thay đổi (Case #2, #3, #4, #5), nhưng **chưa thực hiện trong code**; §9 phải ghi đúng trạng thái này, không ghi như đã làm xong.

