# Đánh giá dữ liệu `fix-gaps/1-Survey.csv`

> Mục đích file này: đánh giá **độc lập với slide**, để nhóm tự quyết định dùng số nào lên slide, số nào không, và biết rõ giới hạn của dữ liệu này trước khi đưa ra ban giám khảo. Không sửa `spec.md`, không sửa file CSV gốc.
>
> Nguồn: `fix-gaps/1-Survey.csv` — khảo sát Google Form, **n = 5 người trả lời**, thời điểm 16/09/2026 19:25–19:29 (5 lượt trả lời trong vòng 4 phút — nhiều khả năng là bạn cùng lớp trả lời tại chỗ, không phải khảo sát trải rộng theo thời gian).

---

## 1. Bảng số liệu đã đếm (đối chiếu lại từ CSV gốc, khớp với số đã cho)

| Câu hỏi | Kết quả (n=5) |
|---|---|
| Gặp khó khăn với workflow "Bài giảng lý thuyết → Ví dụ → Bài tập"? | 5/5 Có |
| Khó ở phần lý thuyết? | 3/5 Có · 2 bỏ trống |
| Khó ở phần thực hành/bài tập? | 4/5 Có · 1 Không |
| Muốn thử làm bài trước khi được giảng lý thuyết? | 5/5 Có — trong đó: 3/5 "Có, nhưng không chắc có hiệu quả hơn không" · 2/5 "Có, tôi nghĩ cách đó hiệu quả hơn" |
| Giả sử có công cụ đưa bài trước lý thuyết, sai thì giải thích đúng chỗ sai — muốn dùng không? | 5/5 Có |
| Điều gì giúp hiểu khái niệm khó nhất? | 3/5 "Tự làm bài tập, mắc lỗi rồi được giải thích" · 2/5 "Đọc / nghe giải thích lý thuyết kỹ" |

**Quote nguyên văn có trong file (chép đúng, không sửa lỗi chính tả):**
- Cột "khó khăn gì": *"Nhiều thông tin"*, *"lí thuyết khó hiểu, dài dòng load chậm "*, *"kiến thức quá nhiều và cảm giác dành cho người đã biết rồi :)))"* — 3 quote có nội dung; 1 người trả lời *"Không có"* (không phải nội dung, là câu trả lời "không có khó khăn gì để nói thêm"); 1 người bỏ trống.
- Cột "muốn cải thiện gì": *"Học nhiều thứ"* — 1 quote có nội dung; 1 người trả lời *"Có"* (không rõ nghĩa, không tính là quote có nội dung); 1 người trả lời *"Không có"*; 2 người bỏ trống.
- **Tổng cộng quote có nội dung thật dùng được: 4** ("Nhiều thông tin", "lí thuyết khó hiểu, dài dòng load chậm", "kiến thức quá nhiều và cảm giác dành cho người đã biết rồi :)))", "Học nhiều thứ"). Các câu "Có"/"Không có" là non-answer, không tính.
- **Nguồn đi kèm mỗi quote:** chỉ có "Dấu thời gian" (vd `16/09/2026 19:25:51`). Form **không thu tên/vai trò người trả lời** — không thể trích dẫn "học viên X nói lúc Y" theo đúng chuẩn nguồn mà `spec.md §1` yêu cầu (turn_id/thời điểm/người nói).

---

## 2. Đánh giá độ mạnh của bằng chứng — đúng mức, không nói quá, không giấu

### 2.1. n=5 là rất nhỏ — trình bày dạng phân số, không quy % và không suy rộng
5 người trả lời trong 4 phút là một mẫu rất mỏng so với quy mô một khoá học (AI20K có nhiều lớp, nhiều học viên hơn 5 người). Bất kỳ diễn đạt kiểu "100% học viên gặp khó khăn" đều **gây ấn tượng sai về quy mô** — con số đúng là "5/5 người được hỏi", không phải "100% học viên khoá AI20K". Kết luận rút ra từ đây **chỉ áp dụng cho 5 người này**, không đại diện cho toàn khoá, không nên dùng để khẳng định quy mô vấn đề (bao nhiêu % học viên toàn khoá gặp vấn đề này).

### 2.2. Câu hỏi "giả sử có công cụ..." là câu hỏi dẫn dắt — bằng chứng YẾU
Câu "Giả sử có một công cụ đưa cho bạn bài tập trước khi học lý thuyết... bạn có muốn sử dụng không?" là một câu hỏi giả định, mô tả sẵn giải pháp và mời người trả lời đồng ý. Loại câu hỏi này gần như luôn ra kết quả đồng thuận cao (5/5 Có ở đây) bất kể người trả lời có thực sự cần hay sẽ dùng công cụ đó không — vì trả lời "Có" cho một ý tưởng nghe hay không tốn gì.

Đối chiếu với phân loại quote ĐẠT/CHƯA ĐẠT (handbook trang 09): quote ĐẠT là lời người dùng nói **lúc đang cố làm một việc thật** (ví dụ: "Mình muốn tìm thông tin về code cho ReAct"); quote CHƯA ĐẠT là lời khen xã giao về một thứ đang được trình bày (ví dụ: "Demo này ok rồi đấy"). Câu trả lời "Có" cho câu hỏi giả định này **gần với loại CHƯA ĐẠT hơn** — thậm chí còn yếu hơn "Demo này ok rồi đấy" một chút, vì người trả lời chưa từng thấy hay dùng công cụ thật, họ chỉ đồng ý với một mô tả bằng lời. Đây **không phải** bằng chứng kiểu "lúc đang cố làm việc thật gặp khó khăn cụ thể".

**Kết luận:** 5/5 "Có" ở câu hỏi giả định này không nên được trình bày như bằng chứng chính về nhu cầu — nó chỉ nói lên rằng ý tưởng "làm sai thì được giải thích" không bị phản đối, chứ không chứng minh học viên thực sự cần hoặc sẽ dùng.

### 2.3. Gộp số làm mất sắc thái — 3/5 là quan tâm có điều kiện, không phải xác nhận giải pháp
Ở câu "muốn thử làm bài trước khi học lý thuyết", nếu chỉ báo cáo "5/5 muốn thử làm bài trước" là **nói quá**. Thực tế:
- 3/5 chọn "Có, **nhưng không chắc có hiệu quả hơn không**" — đây là sự tò mò/quan tâm có điều kiện, chưa phải niềm tin rằng cách đó tốt hơn.
- Chỉ 2/5 chọn "Có, tôi nghĩ cách đó hiệu quả hơn" — đây mới là xác nhận thật.

Nếu lên slide, phải giữ nguyên tỉ lệ 3/5 vs 2/5 này, không gộp thành "5/5 muốn X".

### 2.4. Bằng chứng mạnh nhất thực ra là gì?
Hai điểm mạnh nhất trong bộ dữ liệu này, theo đúng nghĩa "mô tả trải nghiệm/hành vi thật đã xảy ra" chứ không phải phản ứng với một giả định:
1. **5/5 xác nhận gặp khó khăn với workflow lý thuyết → ví dụ → bài tập hiện tại** — đây là câu hỏi về trải nghiệm đã có, không phải giả định, nên là bằng chứng xác nhận pain có thật (dù vẫn chỉ n=5).
2. **3/5 nói "tự làm bài tập, mắc lỗi rồi được giải thích" là điều giúp họ hiểu khái niệm khó nhất** — đây là mô tả một hành vi/cách học đã từng hiệu quả với họ, mạnh hơn câu trả lời cho câu hỏi giả định ở mục 2.2, vì nó dựa trên trải nghiệm học tập thật họ đã có (không nhất thiết là với sản phẩm này, nhưng là với việc "làm rồi sai rồi được sửa" nói chung).

Hai điểm này nên được ưu tiên khi chọn số đưa lên slide, thay vì câu hỏi giả định 5/5.

### 2.5. Độ khớp với problem statement ở `spec.md §1`
Problem statement hiện tại: *"Sau mỗi buổi học, học viên không có cách nào nhanh để tự kiểm tra hiểu đúng/sai với đúng nội dung đã giảng... nên hiểu sai thường không được phát hiện ngay mà tích luỹ sang các buổi sau."* — đây là vấn đề về **thời điểm SAU buổi học**, việc tự kiểm tra hiểu đúng/sai.

Khảo sát này hỏi về hai thứ khác:
- Khó khăn với **thứ tự** của workflow trong buổi học (lý thuyết → ví dụ → bài tập) — đây là vấn đề về **cách dạy trong buổi học**, không hẳn là vấn đề "sau buổi học không có cách tự kiểm tra".
- Muốn **thử làm bài trước khi học lý thuyết** — đây là một đề xuất về **thứ tự học** (thực hành trước, lý thuyết sau — kiểu "flipped"), khác với JTBD hiện tại là "vừa học xong một buổi, muốn biết mình hiểu đúng/sai phần nào".

**Đánh giá thẳng, không gọt cho vừa:** Khảo sát này xác nhận được một pain lớn hơn/liền kề ("học viên thấy khó với cách dạy hiện tại", "học sai/mắc lỗi rồi được sửa giúp hiểu hơn là nghe giảng trước") nhưng **không xác nhận trực tiếp** phần cốt lõi của problem statement đang chốt — là việc **thiếu công cụ tự kiểm tra SAU buổi học** để tránh dồn lỗi sang buổi sau. Không có câu hỏi nào trong form này hỏi "sau khi học xong bạn có biết mình hiểu đúng/sai không", "bạn có tự kiểm tra lại không", hay "lỗi hiểu sai có bị mang sang buổi sau không".

Điểm chung có thật giữa hai bên: cả JTBD và khảo sát đều xoay quanh ý "làm/sai/được giải thích giúp hiểu hơn là chỉ nghe giảng" — đây là điểm khớp thật, hỗ trợ được **cơ chế** của sản phẩm (làm bài, sai thì giải thích). Nhưng **thời điểm** trong JTBD (ngay sau khi học xong một buổi, để không mang lỗi sang buổi sau) chưa được khảo sát này hỏi trực tiếp.

**Khuyến nghị (chỉ ghi khuyến nghị, không tự sửa `spec.md`):** Nhóm nên tự quyết có nên nới câu chữ problem statement để phản ánh đúng hơn bằng chứng đang có ("khó khăn với thứ tự dạy hiện tại" + "thích học qua làm-sai-sửa"), hoặc giữ nguyên problem statement như hiện tại (thời điểm sau buổi học) và coi khảo sát này là bằng chứng **gián tiếp/hỗ trợ cơ chế**, không phải bằng chứng trực tiếp cho đúng câu hỏi "sau buổi học có tự kiểm tra được không". Vì `spec.md` đang trong PR #6 chờ merge, việc này để người dùng/nhóm tự quyết, không tự sửa ở đây.

### 2.6. Vẫn còn thiếu gì so với yêu cầu của `spec.md §1`
`spec.md §1` yêu cầu **≥5 quote nguyên văn + nguồn**. Hiện có:
- **4 quote có nội dung thật** (xem mục 1) — còn thiếu tối thiểu **1 quote nữa** để đạt mốc ≥5, và về chất lượng, 4 quote này đều là cụm từ ngắn (2–10 từ), chưa phải câu mô tả tình huống đầy đủ.
- **Thiếu trường nguồn "người nói"**: form chỉ có Dấu thời gian, không có tên/vai trò/turn_id. Không thể trích dẫn kiểu "học viên A nói lúc...", chỉ có thể trích "một người trả lời khảo sát 16/09/2026 nói...".
- Số liệu % xác nhận: có thể trình bày dạng phân số (n=5) nhưng **không phải là "số liệu mining/kết quả khảo sát" ở quy mô đủ lớn** mà `spec.md §1` mô tả cần "khảo sát tối thiểu học viên khoá AI20K" — 5 người là bước khởi đầu, chưa phải mức tối thiểu đại diện.

### 2.7. Khảo sát này KHÔNG giải quyết được
- **Slide 2 (bảng impact 3 ứng viên):** cần số người, tần suất, chi phí mỗi lần cho từng ứng viên (tự chấm quiz cuối buổi / tóm tắt tự động / hỏi-đáp tự do). Khảo sát này **không hỏi** về tần suất pain xảy ra, không hỏi về "tốn bao nhiêu thời gian/công sức mỗi lần", và không hỏi riêng cho 3 ứng viên đó. Không có cách nào rút số cho bảng impact từ dữ liệu này.
- **Slide 5 (quote từ vòng dùng thử sản phẩm):** khảo sát diễn ra 16/09/2026, **trước khi có sản phẩm** để dùng thử (đây là khảo sát tìm hiểu nhu cầu, không phải khảo sát sau khi dùng công cụ thật). Vì vậy nó **không thể thay thế** validation thật ở slide 5 — không có quote nào ở đây là phản hồi về sản phẩm đã dùng.

---

## 3. Kết luận ngắn

- Bằng chứng **mạnh nhất, dùng được**: 5/5 xác nhận có khó khăn với workflow hiện tại (pain có thật, tuy n nhỏ); 3/5 nói "tự làm rồi sai rồi được sửa" giúp hiểu khái niệm khó nhất (ủng hộ cơ chế sản phẩm).
- Bằng chứng **yếu, không nên làm trọng tâm**: 5/5 "muốn dùng công cụ giả định" — câu hỏi dẫn dắt, gần với lời khen xã giao hơn là nhu cầu thật đã kiểm chứng.
- Còn thiếu để đạt chuẩn `spec.md §1`: ít nhất 1 quote nữa (đang có 4/5), trường nguồn "người nói" (form ẩn danh, chỉ có mốc thời gian), và một vòng khảo sát quy mô lớn hơn để có số liệu đại diện thật cho toàn khoá.
- Không dùng được cho slide 2 (thiếu số impact) và slide 5 (khảo sát trước khi có sản phẩm, không phải phản hồi dùng thử).
