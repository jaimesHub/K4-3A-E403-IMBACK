# Reflection — Nguyễn Công Minh (02774)

> Nhóm I'M BACK · Lớp 3A · Phòng E403 · CP5 · 18/09/2026
> ⚠️ Phần cảm nhận cá nhân bên dưới đang để trống — chờ chính Nguyễn Công Minh tự viết. Không ai viết hộ.

## 1. Bối cảnh (dữ kiện chung, đã điền sẵn)

**VLearn Quiz "Học từ lỗi trước"** — sản phẩm tính năng mới của nhóm I'M BACK (Lớp 3A, Phòng E403, Hướng A/VLearn). Lát cắt: học viên trả lời câu tự luận về buổi học → hệ thống AI đối chiếu nội dung trả lời với transcript bài giảng → trả về nhận định dạng 6 nhãn (đúng, sai, thiếu, ngoài nguồn, không đủ thông tin, khác) kèm giải thích chi tiết và mã trích dẫn `[Txx-NNN]`. Prototype ở mức **Working**, chạy trực tiếp với OpenAI (GPT-4o-mini) hoặc offline mock khi không có API key.

**Đánh giá CP3** (24 câu thử): 21/24 có dẫn nguồn chính xác (87,5%), 3/24 sai, **0 trường hợp bịa mã trích dẫn**. Nhóm tự luận AI chấm 13/16, MCQ 8/8.

**Quality bar CP4** (trên golden set): ≥80% AND 100% nhóm an toàn AND 0 case bịa — **chưa chạy được do thiếu file `transcript-04-clean.md`.**

**Khảo sát 16/09 (n=5)**: 5/5 gặp khó với workflow lý thuyết→ví dụ→bài tập; 3/5 nói "tự làm bài, mắc lỗi rồi được giải thích" giúp hiểu khái niệm khó nhất. **Đo thời gian**: trung bình 30,0 phút/buổi (20–40 phút), cả nhóm đã học AI20K (n=2) và nhóm chưa học (n=3) đều 30,0 phút — không có chênh lệch về thời gian ở cỡ mẫu này.

**Vòng dùng thử (Phần B)**: 5 người ngoài nhóm, 2 người từ CP1 đủ R6. Thu được 5 quote nguyên văn. **4 thay đổi đã quyết định, chưa thực hiện.**

## 2. Vai trò của tôi trong nhóm

🔲 [CHÍNH CHỦ ĐIỀN]
- Bạn đã **chịu trách nhiệm chính** những mảng công việc nào (ví dụ: frontend, dataset, prompt, evaluation)?
- Bạn **làm việc cùng ai** trong nhóm và **cách phối hợp** là như thế nào (ví dụ: họp định kỳ, review code, chia sẻ tài liệu)?
- Bạn có **tham gia quyết định** về **hướng đi kỹ thuật** nào của sản phẩm không (ví dụ: chọn mô hình, chọn API, chọn workflow)?

## 3. Việc tôi trực tiếp làm

🔲 [CHÍNH CHỦ ĐIỀN]
- **Đoạn code hoặc file nào** bạn viết/xây dựng? (ví dụ: hàm gọi OpenAI, logic đối chiếu transcript, UI hiển thị kết quả, data cleaning)
- Bạn **chạy thử hoặc test** sản phẩm bao nhiêu lần? Bạn **phát hiện lỗi nào**, và bạn đã **fix nó hay báo cho người khác**?
- Bạn có **chuẩn bị hoặc kiểm tra dữ liệu** (transcript, golden set, test cases) không? Cụ thể là gì?

## 4. Điều khó nhất tôi gặp phải

🔲 [CHÍNH CHỦ ĐIỀN]
- Khi **test trên 24 câu**, bạn có **tìm ra** một case mà AI trả sai hoặc không phát hiện dấu hiệu gì không? Bạn đã **xác định nguyên nhân** không?
- **Gọi OpenAI API** — bạn có **gặp lỗi** (timeout, rate limit, format sai) hoặc **bất ngờ** (API chậm, kết quả không ổn định)?
- Bạn có **xung đột hoặc mâu thuẫn** nào giữa những gì bạn code với những gì người khác cần không?

## 5. Tôi học được gì về làm sản phẩm AI

🔲 [CHÍNH CHỦ ĐIỀN]
- **Gọi LLM lần đầu** (OpenAI/GPT-4o-mini) — bạn học được điều gì về **cách nó hoạt động** hoặc **hạn chế của nó**?
- Việc **phải đảm bảo không bịa mã trích dẫn** (quality bar khắt khe) đã **thay đổi** cách bạn **thiết kế logic hoặc test** không?
- Qua **khảo sát và vòng dùng thử**, bạn có **thay đổi hiểu biết** về nhu cầu của người học hay **cách AI nên hỗ trợ** không?

## 6. Nếu làm lại, tôi sẽ làm khác chỗ nào

🔲 [CHÍNH CHỦ ĐIỀN]
- Nếu **biết 3 case fail** (CP3-013: ngữ cảnh mỏng; CP3-023, CP3-024: model nhầm nhãn) từ sớm, bạn sẽ **thay đổi gì** (prompt, training data, post-processing)?
- **Bạn có "debt" kỹ thuật nào** (code không gọn, logic phức tạp, test chưa đủ) mà nếu làm lại sẽ sắp xếp khác?
- Nếu có **công việc của bạn chưa hoàn thành** vào CP5 này, bạn sẽ **ưu tiên gì** nếu có thêm thời gian?

## 7. Một điều tôi muốn nói thẳng (khó khăn, bất đồng, điều chưa hài lòng)

🔲 [CHÍNH CHỦ ĐIỀN]
- Bạn có **bất đồng ý kiến** với bất cứ thành viên nào về **hướng đi kỹ thuật** không? Nó được xử lý ra sao?
- Có lúc nào bạn **cảm thấy áp lực** về **deadline, chất lượng, hoặc tài nguyên** không?
- Nếu có điều gì **bạn chưa hài lòng** với **kết quả cuối cùng** (code, tính năng, tài liệu), đó là gì?
