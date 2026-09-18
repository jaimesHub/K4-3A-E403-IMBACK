# Reflection — Lưu Mạnh Hùng (02942)

> Nhóm I'M BACK · Lớp 3A · Phòng E403 · CP5 · 18/09/2026
> ⚠️ Phần cảm nhận cá nhân bên dưới đang để trống — chờ chính Lưu Mạnh Hùng tự viết. Không ai viết hộ.

## 1. Bối cảnh (dữ kiện chung, đã điền sẵn)

**VLearn Quiz "Học từ lỗi trước"** — sản phẩm tính năng mới của nhóm I'M BACK (Lớp 3A, Phòng E403, Hướng A/VLearn). Lát cắt: học viên trả lời câu tự luận về buổi học → hệ thống AI đối chiếu nội dung trả lời với transcript bài giảng → trả về nhận định dạng 6 nhãn (đúng, sai, thiếu, ngoài nguồn, không đủ thông tin, khác) kèm giải thích chi tiết và mã trích dẫn `[Txx-NNN]`. Prototype ở mức **Working**, chạy trực tiếp với OpenAI (GPT-4o-mini) hoặc offline mock khi không có API key.

**Đánh giá CP3** (24 câu thử): 21/24 có dẫn nguồn chính xác (87,5%), 3/24 sai, **0 trường hợp bịa mã trích dẫn**. Nhóm tự luận AI chấm 13/16, MCQ 8/8.

**Quality bar CP4** (trên golden set): ≥80% AND 100% nhóm an toàn AND 0 case bịa — **chưa chạy được do thiếu file `transcript-04-clean.md`.**

**Khảo sát 16/09 (n=5)**: 5/5 gặp khó với workflow lý thuyết→ví dụ→bài tập; 3/5 nói "tự làm bài, mắc lỗi rồi được giải thích" giúp hiểu khái niệm khó nhất. **Đo thời gian**: trung bình 30,0 phút/buổi (20–40 phút), cả nhóm đã học AI20K (n=2) và nhóm chưa học (n=3) đều 30,0 phút — không có chênh lệch về thời gian ở cỡ mẫu này.

**Vòng dùng thử (Phần B)**: 5 người ngoài nhóm, 2 người từ CP1 đủ R6. Thu được 5 quote nguyên văn. **4 thay đổi đã quyết định, chưa thực hiện.**

## 2. Vai trò của tôi trong nhóm

🔲 [CHÍNH CHỦ ĐIỀN]
- Bạn đã **chịu trách nhiệm** những phần hoặc công việc nào trong nhóm (ví dụ: code, spec, testing, data)?
- Bạn **phối hợp** với những người như thế nào để **đảm bảo công việc của bạn kết nối** với phần của người khác?
- Có lúc nào bạn phải **chờ đợi hoặc phụ thuộc vào** công việc của người khác không? Lúc đó bạn làm gì?

## 3. Việc tôi trực tiếp làm

🔲 [CHÍNH CHỦ ĐIỀN]
- **Phần code hoặc spec nào** bạn viết/đóng góp? (ví dụ: prompt engineering, API integration, validation logic, test dataset)
- Bạn đã **chạy/test** sản phẩm bao nhiêu lần, với những **kết quả hoặc phát hiện** nào đáng chú ý?
- Bạn có **giải quyết lỗi hoặc debug** gì không? Nó là lỗi loại nào (logic, API call, data)?

## 4. Điều khó nhất tôi gặp phải

🔲 [CHÍNH CHỦ ĐIỀN]
- Khi **chạy eval trên 24 câu CP3**, bạn có gặp case nào mà **AI trả kết quả sai hoặc không như kỳ vọng** không? Cụ thể là case nào, vì sao sai?
- **3 case fail** (CP3-013, CP3-023, CP3-024) — bạn có **tham gia debug** chúng không? Khó khăn chính là gì (ngữ cảnh mỏng, model nhầm nhãn, dữ liệu thiếu)?
- **Thiếu file `transcript-04-clean.md`** đã khiến golden set không chạy được. Bạn có **đề xuất giải pháp nào** hoặc gặp khó khăn gì trong việc chuẩn bị dữ liệu?

## 5. Tôi học được gì về làm sản phẩm AI

🔲 [CHÍNH CHỦ ĐIỀN]
- Bạn **khám phá ra gì** về cách AI xử lý tự luận (ví dụ: nó hay sai ở đâu, nó cần dữ liệu nào mới tốt)?
- Việc **phải đảm bảo 0 case bịa mã trích dẫn** (quality bar gắt gao) đã **ảnh hưởng** cách bạn thiết kế hoặc test sản phẩm?
- Qua khảo sát (lý thuyết→ví dụ→bài tập) và dùng thử (5 người), bạn có **hiểu rõ hơn** về nhu cầu thực tế của người học không?

## 6. Nếu làm lại, tôi sẽ làm khác chỗ nào

🔲 [CHÍNH CHỦ ĐIỀN]
- Nếu **biết 3 case fail từ sớm** (trước CP4), bạn sẽ **điều chỉnh prompt, data, hoặc logic nào**?
- **4 thay đổi đã quyết định** — nếu bạn là người **thực hiện chúng**, bạn sẽ **ưu tiên cái nào trước** và tại sao?
- Quy trình **test/eval/validation** của bạn có **điểm nào** cần cải thiện để phát hiện lỗi sớm hơn?

## 7. Một điều tôi muốn nói thẳng (khó khăn, bất đồng, điều chưa hài lòng)

🔲 [CHÍNH CHỦ ĐIỀN]
- Bạn có **gặp khó khăn** nào với **tài nguyên, thời gian, hoặc công cụ** khi làm việc không?
- Có lúc nào bạn **không đồng ý** với một quyết định hoặc hướng đi của nhóm không? Bạn xử lý như thế nào?
- Nếu có điều gì **bạn chưa hoàn toàn hài lòng** với kết quả cuối (code, spec, eval), đó là gì và tại sao?
