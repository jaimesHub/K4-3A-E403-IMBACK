# Reflection — Nguyên Ngọc Minh (02653)

> Nhóm I'M BACK · Lớp 3A · Phòng E403 · CP5 · 18/09/2026

## 1. Bối cảnh (dữ kiện chung, đã điền sẵn)

**VLearn Quiz "Học từ lỗi trước"** — sản phẩm tính năng mới của nhóm I'M BACK (Lớp 3A, Phòng E403, Hướng A/VLearn). Lát cắt: học viên trả lời câu tự luận về buổi học → hệ thống AI đối chiếu nội dung trả lời với transcript bài giảng → trả về nhận định dạng 6 nhãn (đúng, sai, thiếu, ngoài nguồn, không đủ thông tin, khác) kèm giải thích chi tiết và mã trích dẫn `[Txx-NNN]`. Prototype ở mức **Working**, chạy trực tiếp với OpenAI (GPT-4o-mini) hoặc offline mock khi không có API key.

**Đánh giá CP3** (24 câu thử): 21/24 có dẫn nguồn chính xác (87,5%), 3/24 sai, **0 trường hợp bịa mã trích dẫn**. Nhóm tự luận AI chấm 13/16, MCQ 8/8.

**Quality bar CP4** (trên golden set): ≥80% AND 100% nhóm an toàn AND 0 case bịa — **chưa chạy được do thiếu file `transcript-04-clean.md`.**

**Khảo sát 16/09 (n=5)**: 5/5 gặp khó với workflow lý thuyết→ví dụ→bài tập; 3/5 nói "tự làm bài, mắc lỗi rồi được giải thích" giúp hiểu khái niệm khó nhất. **Đo thời gian**: trung bình 30,0 phút/buổi (20–40 phút), cả nhóm đã học AI20K (n=2) và nhóm chưa học (n=3) đều 30,0 phút — không có chênh lệch về thời gian ở cỡ mẫu này.

**Vòng dùng thử (Phần B)**: 5 người ngoài nhóm, 2 người từ CP1 đủ R6. Thu được 5 quote nguyên văn. **4 thay đổi đã quyết định, chưa thực hiện.**

## 2. Vai trò của tôi trong nhóm

Tôi phụ trách hai mảng chính: **FE** (`codebase/index.html`) và **eval độc lập** cho grader.

Về FE, tôi làm việc sát với phần backend API — cần liên tục đối chiếu response schema để UI render đúng. Qua đó học được cách Khánh và Hùng thiết kế lớp validation mã `[Txx-NNN]` trong `grader._finalize_grade()` — kiến trúc đơn giản nhưng hiệu quả: đảm bảo bằng code thay vì chỉ tin LLM.

Tôi đề xuất với nhóm nên chạy thêm một bộ eval **độc lập với testset có sẵn** để tránh thiên kiến xác nhận — đề xuất đó dẫn đến việc tôi tự thiết kế và chạy `eval/independent_eval.py` ở giai đoạn cuối.

## 3. Việc tôi trực tiếp làm

**FE (`codebase/index.html`):** Xây toàn bộ UI dạng single-page 6 màn hình (import slide → nhập ngày → generate → quiz → phân tích câu → tổng kết). Dùng vanilla HTML/CSS/JS không framework. Tích hợp badge LIVE/OFFLINE theo `/api/health`, drag-and-drop upload PDF, và render mã `[Txx-NNN]` thành link click được để xem nguyên văn đoạn transcript qua `/api/transcript/{day}/{code}`.

**Eval độc lập (`eval/independent_eval.py`):** Tự thiết kế 23 test case từ nội dung `transcript-01-clean.md` — không đọc `cp3_testset.json` khi viết để tránh thiên kiến. Phủ đủ 6 nhãn verdict + 4 dạng đặc biệt: câu trả lời nghe hợp lý nhưng nhầm fact, câu tự tin bịa thuật ngữ, prompt injection, hỏi thông tin hành chính. Mỗi case có trường `reasoning` ghi rõ tại sao kỳ vọng verdict đó — để người sau kiểm tra được logic của người viết test, không chỉ kiểm tra kết quả.

Kết quả chạy LIVE: **18/23 PASS (78,3%)**. Phát hiện pattern thất bại ở nhóm `ngoai_nguon_du_lieu` — xem mục 4.

## 4. Điều khó nhất tôi gặp phải

**IE-014 và IE-015** là hai case khó nhất: học viên trả lời đúng về chủ đề (multi-agent, RAG) nhưng dùng chi tiết kỹ thuật không có trong transcript — ví dụ "message queue", "vector database", "chunking". Grader trả `mot_phan` thay vì `ngoai_nguon_du_lieu` vì LLM dùng kiến thức nền của mình để xác nhận phần đúng.

Tìm hiểu nguyên nhân: rule trong `grade_text.md` nói "Cấm khẳng định nội dung không có trong transcript" nhưng không có cơ chế kiểm tra tương đương với lớp validate mã `[Txx-NNN]`. Prompt constraint đơn thuần không ngăn được LLM dùng prior knowledge để suy luận — nó chỉ ngăn được hành động có dấu vết cụ thể (như trích một mã cụ thể).

Với **3 case fail CP3** (CP3-013, CP3-023, CP3-024): tôi không phụ trách phân tích trực tiếp nhưng khi đọc lại thấy CP3-013 và IE-009/IE-010 của mình có cùng pattern — grader chấm rộng rãi hơn kỳ vọng khi câu trả lời đúng phần lớn nội dung nhưng thiếu một ý. Ranh giới `dung` vs `mot_phan` là điểm mà cả hai bộ test độc lập đều phát hiện ra cùng một vấn đề.

## 5. Tôi học được gì về làm sản phẩm AI

AI chấm tự luận **giỏi ở cực, yếu ở vùng xám.** Các case rõ ràng (sai hoàn toàn, injection, câu quá ngắn) grader xử lý tốt — đạt 100% ở nhóm `dung`, `sai`, `ngoai_pham_vi`. Nhưng các ranh giới mờ như `mot_phan` vs `dung` hay `ngoai_nguon_du_lieu` vs `mot_phan` lại không ổn định.

Điều quan trọng hơn về chất lượng sản phẩm: **0 case bịa mã** không phải vì LLM tuân thủ prompt — mà vì có lớp code chạy sau LLM để kiểm tra. Đây là bài học thực tế về việc không nên tin hoàn toàn vào LLM để tự enforce constraint của mình.

Khảo sát 5 người + 5 người dùng thử cho thấy người học muốn biết **tại sao sai**, không chỉ **có sai hay không** — đó là lý do phần `explanation` và mã trích dẫn quan trọng hơn verdict_label đơn thuần.

## 6. Nếu làm lại, tôi sẽ làm khác chỗ nào

**Viết test case trước khi có grader**, không phải sau. Tôi thiết kế bộ eval độc lập khá muộn — sau khi pipeline đã ổn định. Nếu làm theo kiểu TDD cho LLM evaluation (viết expected behavior trước, rồi mới viết prompt), sẽ phát hiện vấn đề `ngoai_nguon_du_lieu` vs `mot_phan` từ sớm hơn thay vì chỉ thấy ở cuối.

Với **4 thay đổi đã quyết định nhưng chưa làm**, tôi sẽ ưu tiên cái ảnh hưởng đến độ tin cậy của kết quả trước — cụ thể là thêm bước kiểm tra concept nằm ngoài transcript trước khi cho phép `mot_phan`, vì đây là lỗ hổng ảnh hưởng đến sự tin tưởng của học viên vào kết quả chấm.

Về UI, nên cải thiện màn thông báo lỗi ingest khi PDF không có text layer — hiện tại chỉ có toast ngắn, user không biết bước tiếp theo.

## 7. Một điều tôi muốn nói thẳng (khó khăn, bất đồng, điều chưa hài lòng)

Tôi thấy chưa hài lòng với việc bộ eval CP3 được dùng quá sớm như "số đo chính thức" trong khi testset đó do nhóm tự thiết kế — không có isolation giữa người xây hệ thống và người đo hệ thống. Đây không phải bất đồng với ai cụ thể mà là vấn đề quy trình: khi cùng một nhóm vừa xây grader vừa thiết kế testset, có rủi ro thiên kiến xác nhận dù không cố tình.

Tôi đề xuất chuyện này nhưng không có thời gian để nhóm thảo luận kỹ — cuối cùng tôi tự làm bộ eval độc lập để có thêm một điểm tham chiếu, dù muộn. Nếu làm lại, sẽ nêu vấn đề này sớm hơn và đưa vào quy trình từ đầu, không phải gần cuối.
