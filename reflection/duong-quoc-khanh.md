# Reflection — Dương Quốc Khánh (03013)

> Nhóm I'M BACK · Lớp 3A · Phòng E403 · CP5 · 18/09/2026
> ⚠️ Phần cảm nhận cá nhân bên dưới đang để trống — chờ chính Dương Quốc Khánh tự viết. Không ai viết hộ.

## 1. Bối cảnh (dữ kiện chung, đã điền sẵn)

**VLearn Quiz "Học từ lỗi trước"** — sản phẩm tính năng mới của nhóm I'M BACK (Lớp 3A, Phòng E403, Hướng A/VLearn). Lát cắt: học viên trả lời câu tự luận về buổi học → hệ thống AI đối chiếu nội dung trả lời với transcript bài giảng → trả về nhận định dạng 6 nhãn (đúng, sai, thiếu, ngoài nguồn, không đủ thông tin, khác) kèm giải thích chi tiết và mã trích dẫn `[Txx-NNN]`. Prototype ở mức **Working**, chạy trực tiếp với OpenAI (GPT-4o-mini) hoặc offline mock khi không có API key. 

**Đánh giá CP3** (24 câu thử): 21/24 có dẫn nguồn chính xác (87,5%), 3/24 sai, **0 trường hợp bịa mã trích dẫn**. Nhóm tự luận AI chấm 13/16, MCQ 8/8. 

**Quality bar CP4** (trên golden set): ≥80% AND 100% nhóm an toàn AND 0 case bịa — **chưa chạy được do thiếu file `transcript-04-clean.md`.**

**Khảo sát 16/09 (n=5)**: 5/5 gặp khó với workflow lý thuyết→ví dụ→bài tập; 3/5 nói "tự làm bài, mắc lỗi rồi được giải thích" giúp hiểu khái niệm khó nhất. **Đo thời gian**: trung bình 30,0 phút/buổi (20–40 phút), cả nhóm đã học AI20K (n=2) và nhóm chưa học (n=3) đều 30,0 phút — không có chênh lệch về thời gian ở cỡ mẫu này.

**Vòng dùng thử (Phần B)**: 5 người ngoài nhóm, 2 người từ CP1 đủ R6. Thu được 5 quote nguyên văn. **4 thay đổi đã quyết định, chưa thực hiện.**

## 2. Vai trò của tôi trong nhóm

Là trưởng nhóm, tôi có trách nhiệm định hình chiến lược sản phẩm từ đầu. Cụ thể, tôi đã phải quyết định những tính năng nào sẽ làm dựa trên tasks.md, định nghĩa lát cắt cụ thể, chọn mô hình AI phù hợp, và đặt bar chất lượng cho sản phẩm (≥80% đúng và 0 case bịa mã).

Về phân công, tôi đã giao cho một bạn trách nhiệm chi tiết sản phẩm và thuyết trình; hai bạn còn lại chịu trách nhiệm khảo sát người dùng, đồng thời thực hiện phần giao diện và AI integration. Riêng tôi chịu trách nhiệm chính cho việc dựng base infrastructure và triển khai backend.

Ngoài ra, trong quá trình phát triển, tôi đã phải xử lý những vấn đề lớn như hỗ trợ API key cho các thành viên, định nghĩa golden set cụ thể để phục vụ việc đánh giá sản phẩm, và đảm bảo tích hợp suôn sẻ giữa Frontend và Backend.

## 3. Việc tôi trực tiếp làm

Về mặt kỹ thuật, tôi đã cộng tác với một thành viên khác để định nghĩa chi tiết các tính năng và phạm vi của sản phẩm, phát triển các tính năng trong backend, tích hợp với slides thuyết trình, và viết nội dung slides.

Chịu trách nhiệm chính cho việc chia nhỏ các tính năng thành các task riêng biệt, dựng nền tảng cho Frontend, Backend, và phần AI integration. Đặc biệt, tôi đã triển khai bộ test đánh giá toàn diện dựa trên 24 test case, với kết quả báo cáo chi tiết tại tệp eval/EVAL_REPORT_v1.md. Cụ thể, 21 trên 24 case đạt tiêu chuẩn (87.5% đúng), trong đó: MCQ đạt 8/8, phần tự luận 13/16, không có case nào bịa mã trích dẫn. Ba case trượt là CP3-013, CP3-023, và CP3-024.

## 4. Điều khó nhất tôi gặp phải

Thách thức lớn nhất tôi gặp phải là vấn đề về độ chính xác của AI trong việc phân loại và giải thích. Ba case sai trong eval (CP3-013, CP3-023, CP3-024) phản ánh vấn đề model nhầm lẫn giữa các nhãn "khong_du_thong_tin" và "ngoai_nguon_du_lieu", cùng với một case bị hẹp ngữ cảnh khi trích dẫn. Để khắc phục, tôi cần phải cải thiện system prompt, tối ưu hóa tool calling, và cập nhật lại bộ test đánh giá.

Ngoài ra, vòng dùng thử Phần B với 5 người ngoài nhóm đã tiêu tốn khá nhiều thời gian và công sức trong việc tìm kiếm và liên hệ những người phỏng vấn phù hợp.

Cũng chính vì thời gian khá hạn chế, tôi nhận thấy cần phải phân công rõ ràng hơn cho các thành viên khác để cùng nhau thực hiện khảo sát và thu thập dữ liệu, thay vì để gánh nặng lên một vài người.

## 5. Tôi học được gì về làm sản phẩm AI

Từ lần đầu tiên làm sản phẩm AI (CP1) đến lần này, tôi đã rút ra được nhiều bài học quý báu. Đầu tiên, tôi nên đầu tư nhiều công sức hơn vào khảo sát để thu thập dữ liệu đa dạng, phục vụ tốt hơn cho việc test và đánh giá sản phẩm. Cùng với đó, cần phải định hình rõ ràng các tính năng sẽ xây dựng, xác định các edge case, và nắm bắt những insight nổi bật ngay từ giai đoạn lên kế hoạch.

Thứ hai, việc đặt quality bar từ sớm (≥80% đúng, 0 case bịa) đã giúp quá trình phát triển tính năng và tích hợp AI trở nên rõ ràng và có mục tiêu từ đầu, thay vì vừa phát triển vừa lại phải suy nghĩ về các tiêu chí test và ngưỡng chất lượng.

Thứ ba, về phía golden set, tôi nhận thấy cần phải định nghĩa nhiều test case hơn, cụ thể hơn, và bao gồm nhiều edge case hơn. Tương tự, trong việc khảo sát thực tế người dùng, thay vì chỉ tập trung vào học sinh, sinh viên, và những người làm công nghệ, tôi nên mở rộng hơn để tiếp cận nhiều đối tượng người dùng từ các lĩnh vực khác nhau.

## 6. Nếu làm lại, tôi sẽ làm khác chỗ nào

Nếu được làm lại, tôi sẽ có những thay đổi quan trọng. Thứ nhất, với ba case sai (CP3-013, CP3-023, CP3-024), tôi sẽ chủ động phối hợp với nhóm sớm hơn để thảo luận và tìm ra giải pháp phù hợp, từ đó thể hiện rõ ràng hơn những cải thiện về trải nghiệm người dùng.

Thứ hai, về bốn thay đổi đã quyết định nhưng chưa thực hiện, tôi sẽ để chúng sang CP5 vì thời gian phát triển trong CP3 và CP4 không đủ. Tuy nhiên, nếu có thêm nguồn lực, tôi sẽ ưu tiên chúng hơn.

Thứ ba, về quy trình quản lý và điều phối của nhóm, tôi sẽ cải thiện bằng cách giao task và vai trò cho các thành viên một cách rõ ràng, cụ thể hơn. Đồng thời, tôi sẽ khuyến khích mỗi thành viên chủ động đóng góp ý kiến và tích cực nhận lấy các nhiệm vụ, thay vì chỉ chờ đợi.

## 7. Một điều tôi muốn nói thẳng (khó khăn, bất đồng, điều chưa hài lòng)

Nói một cách thẳng thắn, trong quá trình làm dự án này, không có sự bất đồng ý kiến lớn nào giữa các thành viên nhóm. Ngược lại, mọi người khá hỗ trợ lẫn nhau, và những cuộc thảo luận diễn ra khá sôi nổi và xây dựng.

Về mặt thời gian, tôi dành khoảng 50% cho việc quản lý, điều phối nhóm, và 50% cho việc code, test, debug. Tỷ lệ này là hợp lý cho vị trí trưởng nhóm.

Tuy nhiên, có một điều tôi chưa hoàn toàn hài lòng: mặc dù ý tưởng sản phẩm khá hay, nhưng các nhóm khác chưa thực sự nhìn ra hết tiềm năng của nó. Cụ thể, hệ thống này hoàn toàn có thể được tích hợp với các platform khác nhau và không phụ thuộc vào bất kỳ hệ thống cụ thể nào. Nguyên nhân chính là các nhóm khác chưa đặt ra nhiều câu hỏi; nhóm tôi chưa giải thích rõ ràng đủ lý do và mục đích để các nhóm khác có thể hiểu được tầm quan trọng; và các nhóm khác chưa có cơ hội tự trải nghiệm trực tiếp ứng dụng. Tôi hy vọng ở những dự án tiếp theo, có thể có cơ hội tốt hơn để thể hiện giá trị thực sự của sản phẩm.
