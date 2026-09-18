# 3 — Hướng dẫn thực thi: MỘT buổi thu dữ liệu (Phần A đo thời gian + Phần B dùng thử sản phẩm)

> ⚠️ **File này KHÔNG chứa dữ liệu thu được** — chỉ là checklist thao tác. Không có tên người thử, không có quote, không có số phút nào được điền sẵn ở đây hay ở `fix-gaps/3-BANG-DO-THOI-GIAN.md`/`validation/README.md`. Điền dữ liệu là việc của người chạy buổi này, sau khi chạy xong.
>
> Không commit gì trong lượt tạo file này — CP5 nộp **13:00 hôm nay (18/9)**, lớp 3A · phòng E403 (handbook trang 03). Thiết kế bên dưới nhằm chạy xong trong **30–40 phút tổng cộng**, ưu tiên chạy song song. Không đủ 5 người thì làm được mấy người ghi đúng mấy người — theo handbook trang 06: *"Khai thiếu không bị trừ điểm. Giấu mới bị."*

---

## 0. Vì sao 2 phần này ghép chung một buổi

- **Phần A** (đo thời gian cách cũ) chỉ cần người biết đọc tiếng Việt, ngồi im đọc transcript rồi tự đối chiếu — KHÔNG cần đã học AI20K, KHÔNG cần dùng sản phẩm. Cho ra số thật để thay `⚠️ ước lượng 18–34 phút/buổi` (suy từ độ dài văn bản) trong `spec.md §2`.
- **Phần B** (dùng thử sản phẩm) cần đúng **5 người ngoài nhóm, 2 người đã khai từ CP1** — điều kiện bắt buộc của R6 (8 điểm). Cho ra quote + bảng nhật ký cho `validation/README.md` và slide 5.
- Cùng một người thử có thể làm CẢ HAI phần liên tiếp (~10–12 phút/người) → không cần gọi người 2 lần.

---

## Bước 0 — Kiểm tra nhanh: nhóm có khai willing users ở CP1 chưa (2–3 phút)

**Đã kiểm tra sẵn (git log + `spec.md §8`) để bạn không mất thời gian tra lại:**

- Commit CP1 (`a2793be`, `spec.md` thời điểm đó) chỉ có một dòng khung: *"Willing users (≥2 tên) + kế hoạch vòng validation (bonus, nếu làm)"* — **không có tên nào được điền**.
- `spec.md §8` hiện tại (bản CP5) xác nhận lại: *"⚠️ CHƯA LÀM XONG — repo chưa có danh sách người dùng ngoài nhóm sẵn sàng dùng thử."*
- **Kết luận đã xác minh: nhóm khai 0/2 willing users từ CP1** — không phải do quên ghi vào repo, mà đúng là chưa từng khai ai. Nếu bạn (Khánh) nhớ có nhắn tin/hẹn riêng ai đó ngoài repo (Zalo, Messenger...) hồi CP1 mà lỡ chưa ghi vào file, thì người đó tính là "đã khai từ CP1" — kiểm tra lại trí nhớ/lịch sử chat của mình trong 1 phút. Nếu không nhớ ra ai → coi như thật sự 0/2, đi thẳng sang bước dưới.

**Hành động ngay (không chờ tìm đủ 2 người "hợp lệ" mới bắt đầu):**
1. Vẫn tìm đủ **5 người ngoài nhóm** thật cho Phần B — bạn bè, người học khoá khác, gia đình, ai đang ở gần phòng E403 lúc này.
2. Trong 5 người, đánh dấu người nào **thực sự** từng được nhắc tới/hẹn từ CP1 (nếu có, dù không có trong repo) là "CP1". Nếu không có ai → khai thẳng **0/5 người từ CP1** trong bảng nhật ký, không suy diễn hay gán nhãn "từ CP1" cho người mới gặp hôm nay.
3. Ghi rõ trong `validation/README.md` dòng "Trạng thái hiện tại" con số thật (ví dụ 5/5 người thử, 0/2 hoặc 1/2 hoặc 2/2 từ CP1) — đây là điều duy nhất được sửa ngay, phần còn lại chờ có dữ liệu thật mới điền.

---

## Bước 1 — Chuẩn bị kỹ thuật (5 phút)

1. Khởi động server:
   ```
   cd codebase/backend && python3 -m uvicorn api:app --port 8000
   ```
2. Xác nhận LIVE (không phải OFFLINE):
   ```
   curl http://127.0.0.1:8000/api/health
   ```
   Phải thấy `{"status":"ok","mode":"live","provider":"openai","model":"gpt-4o-mini"}`. Nếu `mode` là `offline` → thiếu API key trong `codebase/backend/.env`, xử lý trước khi làm Phần B (Phần A không cần server, làm được ngay cả khi server offline).
3. Mở `http://127.0.0.1:8000/` trên **đúng MỘT máy/tab** dùng cho toàn bộ Phần B (lý do kỹ thuật ở Bước 3 — không dùng nhiều máy khác nhau cho Phần B).
4. Chọn 1 Day cho Phần A (Day 1 hoặc Day 2 — chọn Day nào ít người trong nhóm đã đọc kỹ để tránh thiên vị). Mở sẵn file transcript tương ứng:
   - Day 1: `output/transcript/transcript-01-clean.md`
   - Day 2: `output/transcript/transcript-02-clean.md`
5. Lấy **3 câu hỏi thật** của đúng Day đó từ `output/quiz.db` (KHÔNG tự đặt câu hỏi mới, KHÔNG generate lại):
   ```
   sqlite3 output/quiz.db "SELECT question, reference_code FROM questions WHERE day=1 ORDER BY RANDOM() LIMIT 3;"
   ```
   (đổi `day=1` thành `day=2` nếu chọn Day 2). Chép 3 câu hỏi (chỉ câu hỏi, KHÔNG kèm `answer`/`explain`) ra giấy hoặc file riêng để đưa người thử — giữ `answer`/`reference` lại cho người bấm giờ, dùng để đối chiếu SAU khi người thử tự chấm xong.
6. Chuẩn bị đồng hồ bấm giờ (điện thoại đủ dùng).
7. In/mở sẵn `fix-gaps/3-BANG-DO-THOI-GIAN.md` để điền trực tiếp trong lúc chạy.

**⚠️ CẢNH BÁO KỸ THUẬT — đọc trước khi làm Phần B:**
Nút **"Generate câu hỏi"** trên UI luôn gọi `POST /api/generate {regenerate: true}`, xoá hết câu hỏi cũ của Day đó và sinh câu hỏi MỚI (question_id mới, câu chữ mới do LLM sinh lại). Nếu bấm nút này cho Day 1 hoặc Day 2, **cả hai Day đều đang được `eval/cp3_testset.json` trỏ tới bằng đúng `question_id` hiện tại** — bấm generate sẽ làm hỏng khả năng tái lập con số 87.5% (21/24) đã chốt. **TUYỆT ĐỐI không bấm nút này cho Day 1/Day 2 trong buổi hôm nay.** Cách vào quiz an toàn ở Bước 3 dưới đây tránh hoàn toàn nút này.

---

## Bước 2 — Phần A: bấm giờ (mỗi người ~5–7 phút, chạy song song được ở nhiều trạm)

**Trước khi bắt đầu, hỏi 1 câu (ghi lại câu trả lời, không dẫn dắt):**
> "Bạn có đang học hoặc đã học khoá AI20K không?"

**Kịch bản đọc nguyên văn cho người thử:**
> "Mình đang muốn đo thử một cách tự kiểm tra hiểu bài sau buổi học. Đây là bản ghi lại nội dung một buổi học (transcript), và đây là 3 câu hỏi liên quan tới buổi đó. Bạn đọc transcript, tìm câu trả lời cho từng câu hỏi trong đầu, rồi **tự đối chiếu lại với đúng đoạn trong transcript** để xem mình trả lời đúng hay sai — không cần viết ra, không cần dùng máy tính hay app gì cả. Bạn làm việc bình thường, khi nào xong đủ 3 câu thì nói cho mình biết. Mình sẽ bấm giờ trong lúc bạn làm — không phải để chấm điểm bạn, chỉ để đo thời gian của cách làm này."

**Thao tác:**
1. Bắt đầu bấm giờ ngay khi người thử cầm/mở transcript và đọc câu hỏi đầu tiên.
2. Không nhắc, không gợi ý trong lúc họ làm. Nếu họ hỏi "câu này đúng không mình đối chiếu vậy đã đủ chưa" → trả lời trung lập: "bạn tự quyết định khi nào thấy đủ chắc".
3. Dừng bấm giờ ngay khi họ nói xong (đã tự đối chiếu đủ 3 câu, tự thấy đúng/sai).
4. Hỏi 1 câu chốt: "Trong 3 câu, bạn tự thấy mình trả lời đúng mấy câu?" — ghi con số họ tự nói, không phải con số bạn chấm hộ.
5. Ghi ngay vào `fix-gaps/3-BANG-DO-THOI-GIAN.md`: tên, có học AI20K không, Day, giờ bắt đầu, giờ kết thúc, tổng phút, số câu tự đánh giá đúng, ghi chú (ví dụ: bị gọi điện giữa chừng, đọc lướt không kỹ...).

---

## Bước 3 — Phần B: dùng thử sản phẩm (mỗi người ~5 phút, chạy song song ở trạm khác Phần A)

### Thiết lập một lần trước khi mời người thử đầu tiên (làm bởi 1 người kỹ thuật, không phải người thử)

Vì nút "Generate câu hỏi" nguy hiểm (xem cảnh báo ở Bước 1), **không cho người thử chạm vào bước Upload/Generate**. Mở sẵn quiz của Day 1 hoặc Day 2 bằng cách gọi trực tiếp API đọc (không đụng `/api/generate`):

1. Mở `http://127.0.0.1:8000/`, mở DevTools Console (F12 → tab Console).
2. Dán và chạy đúng lệnh sau (đổi số `1` thành `2` nếu muốn dùng Day 2):
   ```js
   fetch('/api/quiz/1').then(r=>r.json()).then(qs=>{
     state.generatedDay = 1;
     state.questions = qs;
     state.answers = {};
     startQuiz();
   });
   ```
3. Màn hình sẽ chuyển sang màn "Bắt đầu làm quiz" với đúng bộ câu hỏi thật đang có trong `output/quiz.db` — không có gì bị xoá hay sinh mới (`GET /api/quiz/{day}` chỉ đọc).
4. **Giữ nguyên tab này suốt Phần B** — không F5/refresh, không quay lại bước Upload. Lần lượt để từng người thử ngồi vào tiếp tục trên đúng tab đó. Nếu trang lỡ bị tải lại, chạy lại đúng lệnh console ở trên (vẫn an toàn, chỉ đọc) — **không bấm nút "Generate câu hỏi"** để vào lại quiz.
5. Trả lời câu hỏi (`POST /api/answer`) và xem tổng kết (`POST /api/submit`) đều an toàn, dùng bao nhiêu lần cũng được — hai lệnh này chỉ ghi vào bảng `attempts`, không đụng tới bảng `questions`.

### Kịch bản đọc nguyên văn cho người thử

> "Đây là một web app tự chấm quiz sau buổi học. Trên màn hình đang có sẵn một bộ câu hỏi. Bạn cứ thử trả lời vài câu, xem hệ thống chấm và giải thích ra sao — làm tự nhiên như bạn đang thật sự ôn bài. Mình sẽ ngồi quan sát, không làm gì thêm."

**Sau đó: giao task rồi ngồi im quan sát, đừng hỏi "sản phẩm này hay không"** (handbook trang 09, trích nguyên).

- **Câu CẤM hỏi:** "sản phẩm này hay không?", "bạn thấy ổn chứ?", "có thích không?", "có hữu ích không?", bất kỳ câu nào gợi ý câu trả lời "có/tốt".
- **Câu NÊN hỏi khi họ im lặng quá lâu (>10-15 giây không thao tác gì):** "Bạn đang nghĩ gì vậy?" hoặc "Bạn đang làm gì đó?" — hỏi về hành động, không hỏi về đánh giá.
- **Ghi quote nguyên văn NGAY lúc nghe**, kể cả sai chính tả, kể cả câu chê. Quote ăn điểm là lời nói **lúc đang cố làm một việc** (vd: *"Mình muốn tìm thông tin về code cho ReAct"*), không phải lời khen/chê xã giao (vd: *"Demo này ok rồi đấy"* — KHÔNG tính).
- Ghi lại: họ kẹt ở đâu cụ thể (bấm nhầm gì, đợi lâu ở đâu, không hiểu chữ gì trên màn hình, đọc lại câu hỏi mấy lần...).
- **Chê vẫn tính đủ điểm** — mục đích là tìm ra chỗ chưa ổn để sửa, không phải để lấy lời khen.

---

## Bước 4 — Tổng hợp (10 phút)

1. Điền đầy đủ bảng nhật ký `validation/README.md` (mỗi người thử 1 dòng — Phần B) và `fix-gaps/3-BANG-DO-THOI-GIAN.md` (Phần A).
2. Viết 4 dòng tổng kết cuối bảng ở `validation/README.md` (đã có khung sẵn): chủ đề lặp nhiều nhất · sẽ sửa gì trước demo · giữ nguyên gì và vì sao · gì để dành sau. Chỉ viết dựa trên quote thật vừa ghi, không suy diễn thêm.
3. Chọn **≥1 thay đổi thật** từ feedback vừa nghe (dù nhỏ — ví dụ đổi chữ trên nút, thêm dòng hướng dẫn, đổi vị trí một thành phần UI). Nếu quyết định **giữ nguyên** mọi thứ, phải ghi rõ lý do dựa trên feedback thật (ví dụ: "3/5 người không gặp khó khăn nào ở bước X" — không phải suy đoán).
4. Ghi thay đổi đó vào bảng "Thay đổi đã ghi vào Changelog" trong `validation/README.md`, trỏ đúng dòng nhật ký nào dẫn tới thay đổi.

---

## Bước 5 — Sau khi có dữ liệu thật, cập nhật CHÍNH XÁC các chỗ này

(Không làm trong lượt tạo file hướng dẫn này — làm SAU khi buổi thu dữ liệu xong, dữ liệu đã có thật.)

| # | File | Mục cần sửa | Sửa gì |
|---|---|---|---|
| 1 | `validation/README.md` | Bảng nhật ký + 4 dòng tổng kết + bảng Changelog | Điền dữ liệu thật từ Phần B, xoá các nhãn `🔲 CẦN BỔ SUNG` đã điền xong |
| 2 | `spec.md §2` | Ô "tốn gì mỗi lần" của ứng viên đã chọn | Thay `~18–34 phút/buổi (ước lượng từ độ dài tài liệu)` bằng số đo thật từ `fix-gaps/3-BANG-DO-THOI-GIAN.md` (ghi rõ trung bình + khoảng min–max + **n = mấy người**, giữ nguyên phần ghi chú "đây là số đo hành vi thật, không phải ước lượng" thay cho phần cảnh báo cũ) |
| 3 | `spec.md §9 Changelog` | Thêm 1 dòng mới | Ghi lại: đã bấm giờ thật n người (Phần A) + đã có validation thật với 5 người (Phần B) + ≥1 thay đổi đã áp dụng, trỏ đúng case/quote nào |
| 4 | `CP5_SLIDES_DRAFT.md` | Slide 2 (bảng impact — cột "Số liệu mạnh nhất") | Thay số ước lượng bằng số đo thật (n=mấy người) |
| 4b | `CP5_SLIDES_DRAFT.md` | Slide 5 (User thật nói gì) | Thay toàn bộ khung `🔲 CẦN BỔ SUNG` bằng ≥2 quote thật + thay đổi đã làm |
| 5 | `CP5_GAP_CHECK.md` | Mục 1 (dòng Slide 2 và Slide 5), Mục 2 (dòng 2, 3, 4 của checklist) | Cập nhật trạng thái từ 🔴/🟡 thành 🟢 (hoặc 🟡 nếu vẫn thiếu một phần), ghi rõ còn thiếu gì nếu có |

---

## Phương án tối thiểu nếu không kịp đủ 5 người / đủ thời gian

- Làm được **2–3 người** vẫn có số để trình bày — ghi đúng số thật đã làm được (ví dụ "3/5 người ngoài nhóm, 1/2 từ CP1"), KHÔNG chờ đủ 5 mới bắt đầu tổng hợp.
- Nếu hết giờ mà chưa đủ, khai thẳng trong `validation/README.md` và speaker notes slide 5: số người thật đã làm, số còn thiếu, vì sao thiếu (hết thời gian, không tìm được người) — theo handbook trang 06: *"Khai thiếu không bị trừ điểm. Giấu mới bị."* Không làm R6 đầy đủ thì trần điểm còn 92, nhưng giấu số hoặc bịa quote thì rủi ro nặng hơn nhiều.
- Nếu chỉ kịp 1 trong 2 phần: ưu tiên **Phần B** (điều kiện bắt buộc của R6 = 8 điểm) trước Phần A (chỉ nâng chất lượng 1 ô trong bảng impact, không phải điều kiện bắt buộc).
