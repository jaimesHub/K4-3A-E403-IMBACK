# Transcript Day 04 — LLM Foundation (mock cho eval offline)
# Format: [T04-NNN] nội dung đoạn

[T04-001] AI & LLM Foundation. Bạn đang dùng AI mỗi ngày — nhưng thực sự bên trong nó đang làm gì?

[T04-047] Bản chất của hệ thống Transformer, bản chất của các mô hình ngôn ngữ lớn này, đấy là nó dự đoán. Nó không phải là nó biết cái tri thức đấy, mà là nó đang dự đoán những từ tiếp theo — những token. Đấy là một vòng lặp rất cơ bản: dự đoán, sinh ra, xong append — là thêm vào chuỗi ban đầu — xong lại chạy lại.

[T04-048] Văn bản AI sinh ra nhìn trông rất là có lý, trông rất là thuận mắt, nhưng mà thực ra không phải thế — thực ra nó có thể sai. Đấy sẽ là hiện tượng ảo giác mà các bạn có thể gặp phải — hallucination. Nó sinh ra sai chỉ đơn giản là nó đang cố nối những cái từ với nhau cho có nghĩa thôi.

[T04-049] Token là ngôn ngữ của máy. Con người chúng ta nói chuyện với nhau bằng ngôn ngữ của từ ngữ đúng không? Nhưng mà máy nói chuyện với nhau bằng ngôn ngữ của token. Nó sẽ chẻ nhỏ những cái từ đấy ra thành token — nó không phải là từ, không phải là chữ cái, mà nó là token. Đấy là một đơn vị tính của các mô hình ngôn ngữ lớn: token. Khi nó chẻ thành token thì nó không còn nguyên vẹn một cái từ đấy nữa. Và token này cũng sẽ có sự khác biệt cho từng ngôn ngữ khác nhau. Ví dụ như tiếng Việt thì sẽ tốn hơn tiếng Anh, bởi vì tiếng Việt nó có dấu — nó sẽ tốn hơn khoảng một phẩy mấy lần ấy — 1,3, 1,4 lần.

[T04-050] Token có giá. Các bạn gửi một cái message vào thì các bạn đang trả tiền theo token. Tiếng Việt thì sẽ tốn nhiều token hơn tiếng Anh — chat tiếng Việt thường phải đắt hơn tiếng Anh vì số lượng token nhiều hơn.

[T04-051] Context window — cửa sổ ngữ cảnh — là một mô hình một lúc nó chỉ tiếp nhận được một số lượng nhất định. Khi bạn càng đưa nhiều thông tin, càng đưa nhiều ngữ cảnh, thì cái mô hình càng ngày về sau nó sẽ càng kém đi, và nó sẽ thường quên những thông tin ở lúc đầu.

[T04-052] Context rot — khi context window bị đầy, model bắt đầu quên thông tin ở lúc đầu. Đây là giới hạn kỹ thuật quan trọng khi thiết kế ứng dụng AI thực tế.

[T04-058] Các tham số — parameter — của mô hình. Mình hiểu nôm na parameter này là một cái năng lực mà nó có thể biết. Nó càng nhiều thì tức là nó càng mạnh. Parameter là trọng số (weight) mà model học được trong quá trình huấn luyện, khác hoàn toàn với token.

[T04-059] Reinforcement learning với con người tham gia — viết tắt là RLHF. Hiểu nôm na là bạn đào tạo cái mô hình theo kiểu: nếu nó làm đúng thì nó sẽ được điểm reward, nếu nó làm sai nó sẽ bị trừ điểm. RLHF là kỹ thuật huấn luyện, diễn ra ở giai đoạn train, không phải việc người dùng viết prompt.

[T04-070] Temperature là tham số kiểm soát độ ngẫu nhiên khi model chọn token tiếp theo. Temperature cao thì câu trả lời sáng tạo hơn nhưng kém chính xác hơn.

[T04-071] Top-k sampling: model chỉ chọn trong top-k token có xác suất cao nhất. Điều này giúp giới hạn sự ngẫu nhiên.

[T04-072] Top-p (nucleus) sampling: model chọn trong tập token sao cho tổng xác suất đạt ngưỡng p. Kết hợp với temperature để kiểm soát output.

[T04-088] Mỗi lần bạn gọi API, toàn bộ lịch sử phía trước sẽ được cộng thêm vào context. Model không tự nhớ — bạn phải gửi lại lịch sử mỗi lần.

[T04-089] Lớp đầu tiên là system prompt — lớp gần như có hiệu lực tuyệt đối, vì nó luôn nằm đầu tiên trong mọi prompt bạn truyền vào cho AI; đấy là những câu lệnh mang tính chất quy luật tổng quát, yêu cầu mô hình phải hành động như vậy trong mọi lần.

[T04-090] User prompt là phần người dùng nhập vào mỗi lần tương tác. System prompt đặt khung hành vi, user prompt đặt yêu cầu cụ thể.

[T04-098] Tổng kết Day 04: LLM hoạt động bằng cách dự đoán token tiếp theo, bị giới hạn bởi context window, và hành vi phụ thuộc vào system prompt, RLHF, temperature. Hiểu điều này giúp bạn dùng AI hiệu quả hơn.
