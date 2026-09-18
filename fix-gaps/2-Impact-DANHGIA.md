# Đánh giá gap slide 2 ("Vì sao chọn tính năng này") — bảng impact 3 ứng viên

> Mục đích file này: đánh giá **độc lập với slide/spec**, để nhóm tự quyết định lấp gì bằng số thật, để trống gì, và biết rõ giới hạn trước khi đưa ra ban giám khảo. Không sửa `spec.md §7`, không sửa `fix-gaps/1-Survey.csv`, không đo lại số đã cho.
>
> Nguồn dữ liệu dùng trong file này (đã được cung cấp, không tự đếm lại):
> - `fix-gaps/1-Survey.csv` (n=5, 16/09/2026) + đánh giá độ mạnh ở `fix-gaps/1-Survey-DANHGIA.md`.
> - Độ dài thật của `output/transcript/transcript-01-clean.md` (3.501 từ, 37 đoạn mã) và `transcript-02-clean.md` (5.038 từ, 33 đoạn mã).
> - Số câu hỏi sinh ra thật trong `output/quiz.db` (Day 1 = 10, Day 2 = 10; tổng 14 MCQ + 6 tự luận), chấm MCQ deterministic (không gọi LLM), chấm tự luận qua LLM.

---

## 1. Gap thực chất là gì

`spec.md §2` yêu cầu bảng impact ≥3 ứng viên với 4 cột: **bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi**. Hiện trạng trước khi sửa: cả 3 ứng viên đều `⚠️ chưa có số` ở toàn bộ 4 cột — tức 3×4 = 12 ô trống hoàn toàn.

Sau khi rà lại toàn bộ dữ liệu thật đang có trong repo (khảo sát + đo độ dài transcript + đếm số câu hỏi hệ thống sinh), kết quả: **lấp được một phần rất nhỏ của lưới 12 ô, và chỉ lấp được cho đúng 1 trong 3 ứng viên (ứng viên đã chọn)**. Không có ô nào của 2 ứng viên bị loại lấp được bằng số, vì lý do đơn giản: không có nguồn dữ liệu nào từng đo hoặc hỏi về 2 ứng viên đó.

## 2. Rà từng cột trong 4 cột

| Cột | Lấp được không | Nguồn / vì sao |
|---|---|---|
| **Bao nhiêu người** | **Không lấp được cho bất kỳ ứng viên nào** | Khảo sát n=5 không hỏi riêng "bao nhiêu người gặp vấn đề mà từng ứng viên giải quyết" — 5/5 và 3/5 trong khảo sát là con số về pain chung với workflow học (dùng cho slide 1), không tách theo 3 ứng viên slide 2. Không có số người dùng thật ngoài nhóm (validation chưa có). Không có cách nào rút "bao nhiêu người" từ độ dài transcript hay số câu hỏi hệ thống sinh — hai nguồn đó đo nội dung/hệ thống, không đo con người. → giữ `⚠️ chưa có số` ở cả 3 dòng. |
| **Tần suất** | **Lấp được một phần, chỉ cho ứng viên đã chọn, ở dạng suy ra từ thiết kế hệ thống — không phải đo hành vi** | Tự chấm quiz cuối buổi gắn với lịch học: hệ thống sinh đúng 1 lượt quiz/buổi (Day 1: 10 câu, Day 2: 10 câu — đếm được trong `output/quiz.db`), nên tần suất **thiết kế** là "1 lần/buổi học × số buổi của khoá". Đây là tần suất theo *thiết kế sản phẩm*, không phải tần suất *học viên thực sự dùng* (không ai đo hành vi dùng thật). Với 2 ứng viên loại: không có gì tương tự để suy ra — tóm tắt và hỏi-đáp tự do chưa có bản dựng nào, không có cơ sở tần suất. → 1 dòng có số (kèm chú thích rõ là suy ra từ thiết kế), 2 dòng giữ `⚠️ chưa có số`. |
| **Tốn gì mỗi lần** | **Lấp được, chỉ cho ứng viên đã chọn, bằng ước lượng đo được từ độ dài tài liệu thật** | Đây là cột lấp tốt nhất: so sánh cách cũ (đọc lại toàn bộ transcript buổi học để tự kiểm tra) với số từ đo được thật — Day 1: 3.501 từ/37 đoạn ≈ 18–23 phút đọc lại (150–200 từ/phút); Day 2: 5.038 từ/33 đoạn ≈ 25–34 phút. Đây là **ước lượng suy ra từ độ dài văn bản thật**, giám khảo tự đếm lại được, KHÔNG phải đo bấm giờ hành vi người dùng thật — phải ghi rõ điều này ở mọi nơi con số xuất hiện. Với 2 ứng viên loại: không có gì để đo — tóm tắt tự động và hỏi-đáp tự do không có độ dài/quy trình nào tương ứng đã dựng để đo "tốn gì mỗi lần". → 1 dòng có số (ước lượng, ghi rõ cách tính), 2 dòng giữ `⚠️ chưa có số`. |
| **Khả thi** | **Lấp được cho cả 3, nhưng bằng lý lẽ định tính/kỹ thuật, không phải số đo** | Đây là cột duy nhất `spec.md §2` đã có nội dung định tính từ trước (ứng viên chọn: có đáp án đúng/sai đo được bằng golden set; ứng viên loại 1: không thiết lập được tiêu chí đạt/sai; ứng viên loại 2: phạm vi quá rộng cho lát cắt MỘT CÂU). Đây là đánh giá kỹ thuật/thiết kế có cơ sở (khớp với ràng buộc R4 quality bar, ràng buộc lát cắt MỘT CÂU ở `spec.md §4`), không cần "số" theo nghĩa đo đạc — nhưng cũng không phải "số liệu" đúng nghĩa cột này đòi trong bảng impact. → giữ nguyên như định tính, không đổi thành số giả. |

**Tóm lại:** trong 12 ô của lưới 3×4, lấp được bằng số/ước lượng có nguồn: đúng **2 ô** (tần suất + tốn-gì-mỗi-lần của ứng viên đã chọn). 1 cột (khả thi) có nội dung định tính sẵn cho cả 3 dòng nhưng không phải "số". 9 ô còn lại (toàn bộ cột "bao nhiêu người", và tần suất + tốn-gì-mỗi-lần của 2 ứng viên loại) không có cách lấp trung thực — phải giữ `⚠️ chưa có số`.

## 3. Rủi ro bất đối xứng — đánh giá mức độ và cách xử lý

**Rủi ro có thật và nghiêm trọng ở mức trung bình-cao.** Sau khi lấp, bảng impact sẽ có dạng: dòng "đã chọn" có 2 số thật (dù là ước lượng), 2 dòng "loại" trống hoàn toàn ở cột số liệu, chỉ có lý do định tính. Nhìn thoáng qua, đúng như đề bài cảnh báo tránh — *"trình bày như chỉ có đúng một ý tưởng từ đầu"* — vì bảng sẽ trông như nhóm "đo" được ứng viên mình chọn còn 2 ứng viên kia chỉ nêu ra rồi gạt bỏ bằng lời.

Điều làm rủi ro này **không tệ như nó có thể**, nếu xử lý đúng cách:
- Bản chất câu chuyện thật là: nhóm có 3 ứng viên **thật, cân nhắc trước khi chọn** (đã ghi trong `spec.md §2` từ CP4, không phải thêm vào sau khi thấy số đẹp) — đây là bằng chứng chống lại cáo buộc "chỉ có 1 ý tưởng từ đầu" mạnh hơn là con số. Timestamp/changelog cho thấy 3 ứng viên đã có trước khi có bất kỳ số đo nào.
- Vấn đề thật không phải là "nhóm giả vờ có 3 ý tưởng" mà là "nhóm có 3 ý tưởng thật, nhưng chỉ đo được 1 trong 3" — đây là hai việc khác nhau. Nếu **nói thẳng** sự bất đối xứng này ra (chứ không để bảng tự nói), rủi ro giảm mạnh vì giám khảo thấy nhóm tự nhận biết giới hạn, thay vì phải tự phát hiện ra khoảng trống.

**Cách xử lý đề xuất (đã áp dụng vào slide và spec ở các phần dưới):**
1. Không để 2 dòng loại trống lặng lẽ — ghi rõ bằng chữ (không phải chỉ icon `⚠️`) rằng "2 ứng viên này bị loại bằng lý lẽ định tính/kỹ thuật, không bằng số đo — nhóm chưa đo, không phải nhóm giấu số bất lợi."
2. Trong speaker notes, chủ động nói ra câu tương đương "hai ứng viên kia tụi mình loại bằng lý luận, chưa có số — đây là điểm yếu tụi mình tự nhận" **trước khi** giám khảo hỏi. Chủ động nhận điểm yếu luôn an toàn hơn để bị hỏi rồi mới thừa nhận.
3. Ghi rõ ràng trong cả spec và slide rằng con số 18–34 phút là **ước lượng từ độ dài tài liệu**, không phải đo hành vi thật — nếu lỡ trình bày như số đo hành vi thật mà bị hỏi truy "làm sao đo", nhóm sẽ mất điểm tín nhiệm nặng hơn là cứ để trống.

Kết luận: rủi ro không triệt tiêu được hoàn toàn (dữ liệu thật sự bất đối xứng), nhưng **quản lý được bằng cách nói thẳng** — đúng tinh thần handbook "khai thiếu không bị trừ điểm, giấu mới bị".

## 4. Phương án lấp phần còn thiếu — xếp theo công sức

| # | Phương án | Lấp được gì | Công sức | Kịp trước CP5? |
|---|---|---|---|---|
| 1 | **Thêm câu hỏi tần suất/chi phí vào khảo sát vòng 2** (form ngắn, hỏi riêng cho từng ứng viên: "bạn có muốn tóm tắt tự động không, dùng bao nhiêu lần/buổi", "bạn có hỏi-đáp tự do không, mỗi lần tốn bao lâu") | Cột "bao nhiêu người" + "tần suất" cho cả 3 ứng viên, nếu form thiết kế tốt (tránh câu hỏi dẫn dắt như lần trước) | Thấp–trung (dựng form ~30 phút, chờ người trả lời là biến số lớn nhất — lần trước mất khảo sát xong trong ~4 phút vì mọi người trả lời tại chỗ) | **Có thể kịp** nếu tổ chức được một buổi tại chỗ như khảo sát 1, nhưng phụ thuộc có tiếp cận được người trả lời trước hạn hay không |
| 2 | **Bấm giờ thật 3–5 người đọc lại transcript Day 1/Day 2 rồi tự đối chiếu đúng/sai** | Chuyển ước lượng "18–34 phút" hiện tại từ suy luận độ dài văn bản thành số đo hành vi thật — nâng chất lượng bằng chứng của đúng ô đã lấp, không mở thêm ô mới | Trung bình (cần 3–5 người ngồi đọc thật + bấm giờ, ~30–60 phút mỗi người) | **Có thể kịp** nếu ghép chung với vòng dùng thử 5 người ngoài nhóm đang cần làm cho slide 5/checklist CP5 — tận dụng cùng một nhóm người, đỡ tốn công gọi người 2 lần |
| 3 | **Đo latency/chi phí token thật của sản phẩm khi chạy** (đo qua log `run_quiz_eval.py` hoặc benchmark) | Một góc khác của "tốn gì mỗi lần" — chi phí *của hệ thống* khi chấm, không phải chi phí *của người dùng cách cũ* — bổ sung thêm chiều, không thay thế phương án 1/2 | Thấp (đã có script chạy sẵn, chỉ cần đo thời gian/gọi API trong lúc chạy) — nhưng **không được chạy trong phạm vi việc này** vì đề bài cấm "không chạy server, không gọi API" ở nhiệm vụ này | **Không làm trong lượt này** — để lại làm sau nếu nhóm quyết định, ghi vào phần "còn thiếu" |

**Khuyến nghị:** nếu chỉ chọn một, phương án 2 (bấm giờ thật, ghép với vòng dùng thử) có tỷ lệ công sức/lợi ích tốt nhất vì tận dụng được người đã phải tìm cho slide 5. Phương án 1 lấp được nhiều ô nhất (cả 3 ứng viên) nhưng rủi ro câu hỏi lại dẫn dắt như lần trước nếu không thiết kế kỹ. Phương án 3 không nằm trong phạm vi việc hôm nay.

## 5. Kết luận ngắn cho người viết slide

- Lấp được bằng số/ước lượng có nguồn: tần suất + tốn-gì-mỗi-lần của **ứng viên đã chọn** (dựa trên `output/quiz.db` và độ dài `transcript-01/02-clean.md`).
- Không lấp được, giữ `⚠️ chưa có số` / `🔲 CẦN BỔ SUNG`: cột "bao nhiêu người" cho cả 3 ứng viên; tần suất + tốn-gì-mỗi-lần cho 2 ứng viên loại.
- Phải nói thẳng sự bất đối xứng này trên slide (không để bảng tự lộ ra) và phải ghi rõ số 18–34 phút là ước lượng từ độ dài tài liệu, không phải đo hành vi thật.
