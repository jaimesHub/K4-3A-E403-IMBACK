**CP3 · Video thao tác + số đo:**

**1 · Video thao tác — 30 giây, quay màn hình.** Bấm thật trên sản phẩm, thấy AI trả kết quả thật. Không cần dựng, không cần lồng tiếng.

**2 · Số đo — thử bao nhiêu lần, đúng được bao nhiêu**

Các task cần làm:

1. Vẽ lại workflow sang dạng ảnh

   1. Có bao nhiêu tính năng? tình năng gì? làm việc gì?

      1. Upload/input tài liệu

         1. có thể lấy từ làm mock: [github.com/VinUni-AI20k/K4-3A-Day05-06-AI-Product-Hackathon/tree/main/data/vlearn-pack/slides](https://github.com/VinUni-AI20k/K4-3A-Day05-06-AI-Product-Hackathon/tree/main/data/vlearn-pack/slides)
         2. tạo một folder data lưu
         3. hình thức upload/import vào folder data trong source code
         4. next
      2. Generate Bộ Câu Hỏi, Đáp án, Kèm theo giải thích, Kèm theo trích dẫn(Có AI - LLM tham gia)

         1. Scan tài liệu từ folder Data theo Day hoặc theo một thứ tự tự quy ước
            1. Tạo button để generate 1 day cụ thể đc yêu cầu từ người dùng bằng ô input:
               1. Ví du: ng dùng nhập input số ngày học là "2" + click vào nút generate => hệ thống sẽ lấy value từ user input & tạo ra prompt theo format(tự thiết kế) có sẵn để generate như: Generate bộ câu hỏi day "2"
               2. Lưu lại thông tin Tài liệu tương ứng với Day-X
         2. Setting System_prompt với template/rule tương ứng:
            1. Generate câu hỏi
            2. Generate câu trả lời
            3. giải thích đáp án: rule bao gồm cấu trúc đáp án đúng/sai, giải thích ngắn gọn
            4. Trích xuất trong transcript dạng text: text lý thuyết và mã [Txx-NNN]
         3. Template thì lấy theo mẫu transcript bài giảng tư: [github.com/VinUni-AI20k/K4-3A-Day05-06-AI-Product-Hackathon/tree/main/data/vlearn-pack/transcript](https://github.com/VinUni-AI20k/K4-3A-Day05-06-AI-Product-Hackathon/tree/main/data/vlearn-pack/transcript)
            1. Đọc README.md trước khi chọn transcript: [github.com/VinUni-AI20k/K4-3A-Day05-06-AI-Product-Hackathon/blob/main/data/vlearn-pack/transcript/README.md](https://github.com/VinUni-AI20k/K4-3A-Day05-06-AI-Product-Hackathon/blob/main/data/vlearn-pack/transcript/README.md)
         4. Trả kết quả và lưu vào database(sqllite hoặc csv hoặc md) trong folder ~/output
         5. next
      3. Hiện thị màn hình bắt đầu làm Quiz. Lấy data từ database(sqllite hoặc csv hoặc md) để hiển thị trên giao diện người dùng.

         1. Map câu hỏi, câu trả lời, giải thích và trích xuất lên UI
         2. User thực hiện trả lời câu hỏi
      4. Validate cho câu trả lời loại trắc nghiệm(Không cần AI)

         * Đọc câu trả lời của user
         * Compare với mã code [Txx-NNN] trong file transcript bài giảng tương ứng.
         * Return ra phần giải thích + trich xuất từ database.
      5. Validate cho câu trả lời loại Input Text(Có AI - LLM tham gia)

         1. AI - LLM Đọc câu trả lời của user
         2. AI - LLM Compare với mã code [Txx-NNN] trong file transcript bài giảng tương ứng.
         3. AI - LLM Return ra phần giải thích(có AI trả lời theo template/rule) đáp án.
      6. Summary cuối quiz

         1. Cấu trúc: Thông báo hoàn thành, số câu làm đúng/tổng số câu hỏi, danh sách chi tiết những câu đúng và sai, trích dẫn phần lý thuyết liên quan tới các câu hỏi trong transcript bài giảng.
         2. Nút xem bài giảng: [vlearn.dev/my-courses](https://vlearn.dev/my-courses)
         3. Kiểm tra lại bài sau: đã chuyển tên sang Ôn Tập1.
            1. Loop lại bài quiz từ đầu.
         4. **OPTION**: Khi người dùng làm quiz xong -> học lý thuyết vào bài giảng -> tắt browser đi về -> quay lại ôn tập thì làm thế nào để nhớ được trạng thái user đã hoàn thành bài quiz trước đó, giờ chỉ cần ôn tập lại?
            1. Tạm thời có thể lưu kết quả làm quiz + trạng thái xác định đã làm quiz vào local storage trên browser
            2. Advanced có thể suy nghĩ và làm sau nếu có thời gian: tạo bảng user + bảng kết quả làm quiz riêng trong database
               1. Login / Logout
               2. Phân quyền
               3. ....
   2. Có bao nhiêu màn hình? mỗi màn hình làm gì? Luồng chạy bắt đầu từ màn nào và đi tới đâu?

      1. Input tài liệu
         1. Có 3 step:
            1. Import/upload tài liệu bài giảng
            2. Generate bộ câu hỏi
            3. Thông báo genera thành công + Nút bắt đầu làm quiz
      2. Bắt đầu làm quiz
      3. Chi tiết câu hỏi
         1. Trắc nghiệm
         2. Tự luận Input Text
      4. Summary
2. Liệt kê kiến trúc, thiết kế cho từng bước trong workflow

   1. Database: sql-lite hoặc csv hoặc md
      1. Cần lưu thông tin:
         1. ID - timestamp
         2. Question - string
         3. Answer - string
         4. Explain - string
         5. Reference - string - nội dung trích dẫn
         6. ReferenceCode - string - [Txx - nnn]
         7. ReferenceURL - string - đường đẫn tới file transcript
3. Vide Coding + Review + Self Test
4. Quay video sản phẩm(đã tích hợp LLM)
5. Chuẩn bị danh sách các câu hỏi(test case) để đo benchmark sản phẩm
6. Ghi nhận kết quả sau benchmark
7. Nộp bài
