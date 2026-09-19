# Reflection - Lưu Mạnh Hùng (02942)

> Nhóm I'M BACK · Lớp 3A · Phòng E403 · CP5 · 19/09/2026

## 1. Bối cảnh (dữ kiện chung, đã điền sẵn)

**VLearn Quiz "Học từ lỗi trước"** - sản phẩm tính năng mới của nhóm I'M BACK (Lớp 3A, Phòng E403, Hướng A/VLearn). Lát cắt: học viên trả lời câu tự luận về buổi học → hệ thống AI đối chiếu nội dung trả lời với transcript bài giảng → trả về nhận định dạng 6 nhãn (đúng, sai, thiếu, ngoài nguồn, không đủ thông tin, khác) kèm giải thích chi tiết và mã trích dẫn `[Txx-NNN]`. Prototype ở mức **Working**, chạy trực tiếp với OpenAI (GPT-4o-mini) hoặc offline mock khi không có API key.

**Đánh giá CP3** (24 câu thử): 21/24 có dẫn nguồn chính xác (87,5%), 3/24 sai, **0 trường hợp bịa mã trích dẫn**. Nhóm tự luận AI chấm 13/16, MCQ 8/8.

**Quality bar CP4** (trên golden set): ≥80% AND 100% nhóm an toàn AND 0 case bịa - **chưa chạy được do thiếu file `transcript-04-clean.md`.**

**Khảo sát 16/09 (n=5)**: 5/5 gặp khó với workflow lý thuyết→ví dụ→bài tập; 3/5 nói "tự làm bài, mắc lỗi rồi được giải thích" giúp hiểu khái niệm khó nhất. **Đo thời gian**: trung bình 30,0 phút/buổi (20–40 phút), cả nhóm đã học AI20K (n=2) và nhóm chưa học (n=3) đều 30,0 phút - không có chênh lệch về thời gian ở cỡ mẫu này.

**Vòng dùng thử (Phần B)**: 5 người ngoài nhóm, 2 người từ CP1 đủ R6. Thu được 5 quote nguyên văn. **4 thay đổi đã quyết định, chưa thực hiện.**

## 2. Vai trò của tôi trong nhóm

Vai trò của tôi là "Tổng hợp thông tin, BE". Trong thực tế, việc đầu tiên tôi làm cũng đúng như vậy: sáng 17/09, tôi ngồi bóc tách toàn bộ ý tưởng của nhóm thành một bản kế hoạch chi tiết ở `tasks.md` - có bao nhiêu tính năng, bao nhiêu màn hình, luồng đi từ màn nào sang màn nào, và cả cấu trúc dữ liệu cần lưu (câu hỏi, đáp án, giải thích, đoạn trích, mã `[Txx-NNN]`, đường dẫn nguồn). Cùng lúc tôi chuẩn bị sẵn phần hạ tầng để đo chất lượng sau này: `eval/golden_set.json` (25 case) và `eval/goldenSetReq.md`.

Bản `tasks.md` đó gần như là khung xương để Khánh (trưởng nhóm) dựa vào dựng backend thật ngay sau đó (commit `70424b1`, `687c8b4`...). Đây là chỗ tôi thấy rõ nhất việc "phối hợp": mình không code song song với Khánh, mà đưa ra bản kế hoạch trước, Khánh code theo, còn mình theo dõi qua các commit tiếp theo để đối chiếu xem sản phẩm có đi đúng với workflow đã vạch không. Từ sau khi nộp phần khung này, phần lớn việc dựng pipeline, chạy LIVE, viết báo cáo đo lường... rơi vào tay Khánh - tôi ở thế phải chờ và theo dõi nhiều hơn là trực tiếp code tiếp, điều này tôi nói rõ hơn ở mục 7.

## 3. Việc tôi trực tiếp làm

Theo đúng git log, tôi có một commit chính (`c4b828e`, 17/09 12:05): thêm `tasks.md`, `eval/golden_set.json` (25 case), `eval/goldenSetReq.md`, khởi tạo `eval/run_results.md` (file rỗng, để chỗ ghi log sau này), và một bản `codebase/index.html` - giao diện tĩnh dựng nhanh để cả nhóm hình dung layout trước khi có backend thật.

Tôi không phải người trực tiếp chạy benchmark LIVE hay viết `eval/EVAL_REPORT_v1.md` - phần đó Khánh làm (commit `a2d829e`, `3d35c42`). Phần việc tôi chuẩn bị, bộ golden set 25 case.

## 4. Điều khó nhất tôi gặp phải

Ba case trượt ở CP3 (CP3-013, CP3-023, CP3-024) tôi và Khánh trực tiếp debug - phần phân tích đó nằm trong `eval/EVAL_REPORT_v1.md` chạy và ghi lại. Đọc báo cáo thì thấy khá rõ: CP3-013 do ngữ cảnh trích dẫn quá ngắn khiến AI chấm rộng tay hơn kỳ vọng; còn CP3-023 và CP3-024 là AI nhầm giữa hai nhãn gần nghĩa - "không đủ thông tin" và "ngoài nguồn dữ liệu" - vì ranh giới hai nhãn này chưa được mô tả đủ rõ trong prompt.

## 5. Tôi học được gì về làm sản phẩm AI

Đọc `EVAL_REPORT_v1.md` tôi mới thấy rõ: chỉ cần hai nhãn có ranh giới ngữ nghĩa gần nhau (như "không đủ thông tin" vs "ngoài nguồn dữ liệu") mà prompt không cho ví dụ cụ thể, model rất dễ nhầm - không thể để AI tự suy luận ranh giới, phải viết rõ ra.

Việc quality bar bắt "0 case bịa mã trích dẫn" cũng khiến tôi khi soạn golden set phải cẩn thận hơn nhiều: chốt `expected_verdict` và mã trích dẫn tương ứng cho từng case ngay từ đầu, trước khi biết AI sẽ trả lời gì. Lúc đầu tôi thấy hơi mất công, nhưng giờ hiểu tại sao nhóm bắt buộc phải "chốt chuẩn trước khi chạy" thay vì nhìn kết quả rồi mới chỉnh chuẩn cho khớp.

Qua đợt khảo sát và dùng thử thật (5 người), tôi thấy rõ có những pain không nằm trong phần mình vạch ra ở `tasks.md` ban đầu - ví dụ như không có progress bar lúc generate quiz, hay câu trả lời AI bị chê "hàn lâm" quá. Lúc lên kế hoạch ban đầu tôi chỉ tập trung vào luồng chức năng (có màn nào, lưu gì), chưa nghĩ tới trải nghiệm chờ đợi hay cách AI diễn đạt - đây là bài học rõ nhất.

## 6. Nếu làm lại, tôi sẽ làm khác chỗ nào

Tôi sẽ lấy file `transcript-04-clean.md` ngay từ lúc soạn golden set, thay vì để đến gần CP5 mới lộ ra là thiếu. Đáng lẽ chỉ cần thử chạy script `run_quiz_eval.py` một lần ngay từ đầu (kể cả chưa có kết quả chính thức) là đã phát hiện được vấn đề thiếu file sớm hơn nhiều.

Nếu là người thực hiện 4 thay đổi đã quyết định từ feedback, tôi sẽ ưu tiên Case #4 (viết lại `grade_text.md` để giảm ngôn ngữ hàn lâm) trước, vì đây là thay đổi đã có hướng sửa rõ nhất và đánh trúng đúng lỗi nhầm nhãn đã thấy trong EVAL_REPORT - sửa một chỗ nhưng giải quyết được cả vấn đề trải nghiệm lẫn chất lượng chấm.

## 7. Một điều tôi muốn nói thẳng (khó khăn, bất đồng, điều chưa hài lòng)

Khó khăn thật nhất là giai đoạn phân tích pain point và dựng khung ý tưởng cũng như workflow bạn đầu. Việc này sẽ định hướng team sẽ phát triển ứng dụng như thế nào ở các giai đoạn sau. Chúng tôi tốn khá nhiều thời gian để thảo luận, phân tích làm rõ việc trên. Quá trình thuyết trình chưa làm nổi bật những điểm khác biết, sự tiện dụng, tính đơn giản của sản phẩm. Đây là những bài học sâu sắc mà tôi cũng như cả team cần cải thiện cho những bài tập nhóm sau này.
