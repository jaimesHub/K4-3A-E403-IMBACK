# Reflection — Hoàng Công Minh (02774)

> Nhóm I'M BACK · Lớp 3A · Phòng E403 · CP5 · 18/09/2026
> Reflection cá nhân của Hoàng Công Minh, viết dựa trên phần việc khảo sát và hỗ trợ kiểm tra trải nghiệm sản phẩm.

## 1. Bối cảnh (dữ kiện chung, đã điền sẵn)

**VLearn Quiz "Học từ lỗi trước"** — sản phẩm tính năng mới của nhóm I'M BACK (Lớp 3A, Phòng E403, Hướng A/VLearn). Lát cắt: học viên trả lời câu tự luận về buổi học → hệ thống AI đối chiếu nội dung trả lời với transcript bài giảng → trả về nhận định dạng 6 nhãn (đúng, sai, thiếu, ngoài nguồn, không đủ thông tin, khác) kèm giải thích chi tiết và mã trích dẫn `[Txx-NNN]`. Prototype ở mức **Working**, chạy trực tiếp với OpenAI (GPT-4o-mini) hoặc offline mock khi không có API key.

**Đánh giá CP3** (24 câu thử): 21/24 có dẫn nguồn chính xác (87,5%), 3/24 sai, **0 trường hợp bịa mã trích dẫn**. Nhóm tự luận AI chấm 13/16, MCQ 8/8.

**Quality bar CP4** (trên golden set): ≥80% AND 100% nhóm an toàn AND 0 case bịa — **chưa chạy được do thiếu file `transcript-04-clean.md`.**

**Khảo sát 16/09 (n=5)**: 5/5 gặp khó với workflow lý thuyết→ví dụ→bài tập; 3/5 nói "tự làm bài, mắc lỗi rồi được giải thích" giúp hiểu khái niệm khó nhất. **Đo thời gian**: trung bình 30,0 phút/buổi (20–40 phút), cả nhóm đã học AI20K (n=2) và nhóm chưa học (n=3) đều 30,0 phút — không có chênh lệch về thời gian ở cỡ mẫu này.

**Vòng dùng thử (Phần B)**: 5 người ngoài nhóm, 2 người từ CP1 đủ R6. Thu được 5 quote nguyên văn. **4 thay đổi đã quyết định, chưa thực hiện.**

## 2. Vai trò của tôi trong nhóm

Tôi phụ trách phần khảo sát và hỗ trợ kiểm tra trải nghiệm frontend của VLearn Quiz. Tôi nhìn luồng sản phẩm từ góc độ người học: chọn buổi học, tạo quiz, làm câu hỏi và đọc phần giải thích sau khi trả lời. Tôi phối hợp với các bạn làm frontend/backend để phản hồi những điểm dễ gây nhầm lẫn trong luồng này, đồng thời cùng nhóm tổng hợp kết quả khảo sát để kiểm tra xem ý tưởng “làm bài, sai rồi được giải thích” có phù hợp với nhu cầu học hay không.

Tôi ủng hộ việc giữ lát cắt hẹp: không làm trợ lý trả lời mọi câu hỏi, mà tập trung vào quiz sau buổi học có đối chiếu transcript và mã trích dẫn. Nhờ vậy người dùng biết mình đang làm bài nào, AI dựa vào đâu để nhận xét và cần xem lại phần nào khi trả lời sai.

## 3. Việc tôi trực tiếp làm

Tôi tham gia thu thập và đọc lại dữ liệu khảo sát 5 người ngày 16/09. Kết quả đáng chú ý là 5/5 người được hỏi cho biết gặp khó với workflow lý thuyết → ví dụ → bài tập; 3/5 cho rằng tự làm bài, mắc lỗi rồi được giải thích là cách giúp họ hiểu khái niệm khó nhất. Tôi dùng các tín hiệu này để kiểm tra tính hợp lý của luồng quiz và phần phản hồi sau mỗi câu.

Khi thử giao diện, tôi kiểm tra các bước chính: chọn Day, tạo quiz, làm câu trắc nghiệm/tự luận, nhận nhận xét và xem mã trích dẫn. Tôi đặc biệt chú ý rằng người dùng cần thấy rõ giới hạn đầu vào và lý do khi một thao tác không thực hiện được; phản hồi từ vòng dùng thử cũng cho thấy việc giới hạn định dạng upload dễ làm người dùng bối rối. Tôi đã phản ánh các điểm này cho nhóm để đưa vào danh sách cải thiện UX. Tôi không phụ trách phần gọi OpenAI API hay logic chấm điểm, nên không nhận phần việc kỹ thuật đó.

## 4. Điều khó nhất tôi gặp phải

Khó nhất với tôi là phân biệt giữa phản hồi tích cực về ý tưởng và bằng chứng cho một nhu cầu thật. Khảo sát có mẫu nhỏ (n=5), lại có những câu hỏi giả định, nên không thể dùng kết quả đó để khẳng định cho toàn bộ học viên. Tôi học cách giữ nguyên phạm vi kết luận: dữ liệu chỉ cho thấy tín hiệu ban đầu rằng cách học qua làm–sai–được giải thích đáng để thử.

Khi xem báo cáo 24 case, tôi cũng thấy rõ một khó khăn khác: hệ thống đạt 21/24 và không bịa mã trích dẫn, nhưng vẫn sai nhãn ở CP3-013, CP3-023 và CP3-024. CP3-013 cho thấy ngữ cảnh đưa cho model quá ngắn; hai case còn lại cho thấy model chưa phân biệt tốt giữa “không đủ thông tin” và “ngoài nguồn dữ liệu”. Điều này làm tôi nhận ra giao diện có rõ ràng đến đâu cũng không bù được cho một quyết định AI thiếu chính xác; chất lượng phải được kiểm tra ở cả dữ liệu, prompt và trải nghiệm hiển thị kết quả.

## 5. Tôi học được gì về làm sản phẩm AI

Tôi học được rằng LLM không phải bộ chấm điểm tuyệt đối. Nó có thể tạo nhận xét hữu ích, nhưng rất nhạy với ngữ cảnh được cung cấp và cách mô tả nhãn trong prompt. Vì vậy, phần phản hồi AI cần đi cùng bằng chứng người học kiểm tra được, thay vì chỉ hiện một kết luận chung chung.

Yêu cầu không được bịa mã trích dẫn là điểm tôi đánh giá cao nhất trong thiết kế sản phẩm. Kết quả CP3 cho thấy 0/24 case bịa mã, dù vẫn còn ba case sai nhãn. Điều đó cho thấy nhóm đã tách được hai việc: kiểm soát nguồn dẫn và cải thiện độ đúng của phân loại. Với người học, một lời giải thích có mã `[Txx-NNN]` để quay lại transcript đáng tin hơn rất nhiều so với câu trả lời AI không có căn cứ.

Từ khảo sát và dùng thử, tôi hiểu rằng AI nên hỗ trợ đúng thời điểm người học vừa làm sai: chỉ ra điểm cần xem lại, nói rõ giới hạn của hệ thống và hướng dẫn bước tiếp theo. Không nên giả định rằng người dùng đã hiểu thuật ngữ kỹ thuật hoặc biết trước định dạng dữ liệu mà sản phẩm hỗ trợ.

## 6. Nếu làm lại, tôi sẽ làm khác chỗ nào

Nếu làm lại, tôi sẽ làm khảo sát sớm hơn và thiết kế câu hỏi bám trực tiếp vào vấn đề sau buổi học: người học có tự biết mình sai ở đâu không, họ mất bao lâu để tự kiểm tra, và họ đang làm gì khi bị kẹt. Tôi cũng sẽ thu tên hoặc mã ẩn danh của người trả lời (có đồng ý) để mỗi quote có nguồn rõ ràng hơn, thay vì chỉ có thời gian phản hồi.

Về sản phẩm, tôi sẽ ưu tiên chạy golden set ngay khi có đủ transcript, rồi dùng kết quả để sửa prompt và bổ sung ví dụ đối lập cho hai nhãn `khong_du_thong_tin` và `ngoai_nguon_du_lieu`. Với CP3-013, tôi sẽ đề xuất lấy ngữ cảnh rộng hơn thay vì chỉ dùng một đoạn trích ngắn. Ở frontend, tôi sẽ ưu tiên thông báo rõ các định dạng được hỗ trợ, trạng thái đang xử lý và cách khắc phục khi upload thất bại trước khi thêm tính năng mới.

## 7. Một điều tôi muốn nói thẳng (khó khăn, bất đồng, điều chưa hài lòng)

Tôi không có bất đồng lớn với nhóm về hướng đi, nhưng có áp lực về thời gian vì nhiều phần cần vừa làm vừa kiểm chứng. Điều tôi chưa hài lòng nhất là chuẩn chất lượng chính thức trên golden set chưa chạy được do thiếu `transcript-04-clean.md`. Con số 87,5% trên 24 case CP3 là hữu ích, nhưng không thể thay thế kết quả golden set 25 case với các điều kiện chặt hơn.

Tôi cũng nghĩ nhóm có thể làm tốt hơn ở phần bằng chứng người dùng: khảo sát n=5 và vòng dùng thử là một khởi đầu tốt, nhưng còn nhỏ và một số thay đổi sau phản hồi mới dừng ở quyết định, chưa kịp triển khai. Dù vậy, tôi đánh giá tích cực việc nhóm ghi nhận thẳng các giới hạn này thay vì trình bày kết quả như thể sản phẩm đã hoàn thiện. Nếu có thêm thời gian, tôi muốn ưu tiên hoàn tất vòng đo chính thức và kiểm tra lại trải nghiệm sau khi các cải thiện UX được áp dụng.
