# CP3 — Video thao tác + Số đo

> Tài liệu này gom lại đúng 2 sản phẩm giao nộp CP3 theo `handbook.pdf` trang 05 +
> `CHECKLIST.md`: (1) kịch bản quay video thao tác 30 giây, (2) bảng số đo
> "thử bao nhiêu, đúng bao nhiêu" cùng cách tái lập toàn bộ pipeline từ đầu.

## 0. Điều kiện tiên quyết — PHẢI làm trước khi quay

Video CP3 **bắt buộc** có ít nhất 1 lời gọi AI chạy thật (không phải mock).

> **Cập nhật 2026-09-17:** `codebase/backend/.env` **đã có** `OPENAI_API_KEY`
> thật. Đã xác nhận `curl http://127.0.0.1:8000/api/health` trả
> `{"status":"ok","mode":"live","provider":"openai","model":"gpt-4o-mini"}`.
> Bộ câu hỏi Day 1 + Day 2 đã được generate lại bằng LLM thật
> (`POST /api/generate {regenerate:true}`) — đây là lần đầu bộ câu hỏi trong
> `output/quiz.db` được sinh bởi LLM thật thay vì mock offline. Số đo LIVE đầy
> đủ nằm ở §2.2 bên dưới. Việc còn lại trước khi nộp bài là **quay video** theo
> kịch bản §1 (người dùng tự quay) — server cần đang chạy ở `mode: live` lúc
> quay.

Các bước dưới đây vẫn giữ nguyên làm tài liệu tái lập cho người khác trong
nhóm (hoặc nếu key hết hạn/đổi máy):

1. Mở `codebase/backend/.env`, điền **một** trong các key sau (khuyến nghị
   `OPENROUTER_API_KEY` — rẻ, đa model):
   ```
   OPENROUTER_API_KEY=sk-or-...
   ```
2. Khởi động lại server (xem lệnh ở §3).
3. Xác nhận LIVE thật: `curl http://127.0.0.1:8000/api/health` phải trả về
   `"mode":"live"` (không phải `"offline"`). Badge trên UI (góc phải trên
   cùng) sẽ chuyển sang **"● LIVE — provider · model"** màu xanh lá.
4. Generate lại bộ câu hỏi bằng LLM thật cho ngày sẽ demo (nút "✨ Generate
   câu hỏi" trên UI tự làm việc này qua `POST /api/generate {regenerate:true}`
   — không cần làm tay).

**Không quay video khi badge còn hiện "OFFLINE (mock)"** — video sẽ không
được tính vì không có bằng chứng AI chạy thật.

## 1. Kịch bản quay video — 30 giây, quay màn hình, bấm thật

Không dựng, không lồng tiếng, không cắt ghép. Quay liên tục một lần từ màn
`s-import` tới lúc thấy AI trả kết quả có trích dẫn.

| Giây | Bấm gì | Thấy gì (bằng chứng) |
|---|---|---|
| 0–2 | Mở `http://127.0.0.1:8000/` | Badge góc phải trên **"● LIVE — <provider>:<model>"** màu xanh lá — bằng chứng đầu tiên AI đang chạy thật |
| 2–6 | Kéo/thả (hoặc bấm chọn) file `data/slides/d1-slide-hackathon.pdf`, bấm **"Tiếp theo →"** | File hiện trong danh sách với trạng thái **"✓ đã lưu · Day 1"** (từ `POST /api/upload` thật) |
| 6–9 | Gõ số **1** vào ô "Nhập số ngày học", bấm **"✨ Generate câu hỏi"** | Chuyển màn loading, dòng trạng thái đổi qua từng bước: "Đang trích xuất transcript...", "Đang gửi yêu cầu sinh câu hỏi tới AI (chế độ LIVE — ...)" |
| 9–13 | Chờ (server gọi `POST /api/ingest` rồi `POST /api/generate` thật) | Màn "🎉 Generate thành công!" hiện đúng số câu MCQ/tự luận thật + dòng "Chế độ AI khi sinh: LIVE (...)" |
| 13–15 | Bấm **"🚀 Bắt đầu làm quiz →"** | Vào màn quiz, thấy câu hỏi thật lấy từ `GET /api/quiz/1` |
| 15–17 | Bấm chuyển tới **một câu tự luận** (nếu câu đầu là MCQ, bấm "Câu tiếp →" cho tới khi thấy badge **✏️ Tự luận**) | Câu hỏi tự luận hiện ra |
| 17–22 | Gõ một câu trả lời (ví dụ diễn giải lại ý chính của đoạn được hỏi), bấm **"✨ Gửi cho AI chấm →"** | Màn "AI đang đánh giá câu trả lời... bằng AI thật (provider:model)" — đây là lời gọi AI chạy thật thứ hai (`POST /api/answer`, route qua LLM live vì `qtype=text`) |
| 22–28 | Chờ AI chấm xong | Màn phân tích hiện **nhận định** (đúng/sai/một phần...) + **giải thích do AI viết** + khối "📖 Trích dẫn từ transcript" với mã **`[Txx-NNN]`** thật (bấm vào mã để thấy `GET /api/transcript/...` trả đúng nội dung) |
| 28–30 | Bấm **"Xem kết quả 🏁"** | Màn tổng kết hiện điểm số thật lấy từ `GET /api/summary/1` |

Khoảnh khắc **bắt buộc phải lọt vào video**: giây 17–28 — gửi một câu tự luận
và thấy AI (LIVE) trả lời kèm mã trích dẫn `[Txx-NNN]`. Đây là qtype duy nhất
thực sự đi qua LLM (MCQ được chấm deterministic, không gọi AI — xem
`codebase/backend/vlearn/grader.py::grade_mcq`).

## 2. Số đo — "thử bao nhiêu, đúng bao nhiêu"

Bộ câu thử: `eval/cp3_testset.json` — **24 case** (≥ 20 theo yêu cầu handbook),
dựng trên đúng các câu hỏi thật đang có trong `output/quiz.db` (Day 1 + Day 2,
sinh bằng chính `POST /api/generate`), phủ đủ các nhóm: MCQ đúng/sai, tự luận
đúng/một phần/sai, tự luận quá mơ hồ, tự luận đòi hỏi ngoài phạm vi (prompt
injection/hành chính), tự luận lạc đề hoàn toàn (không có căn cứ trong
transcript). Chạy bằng `eval/cp3_benchmark.py` — gọi thật `POST /api/answer`
qua HTTP, không mock trong script.

**Định nghĩa ĐẠT của 1 case:** `verdict_label` API trả về khớp
`expected_verdict` trong testset, **VÀ** không có mã `[Txx-NNN]` bịa
(`validation.invalid_codes` rỗng).

### 2.1. Lượt chạy OFFLINE (mock) — đã chạy, KHÔNG phải số nộp CP3

> ⚠️ Chạy lúc `.env` chưa có API key → server ở `mode: offline`. Con số này
> chỉ chứng minh pipeline + testset chạy đúng end-to-end qua HTTP thật; **không
> được dùng làm số nộp CP3** vì không có lời gọi AI thật.

**Thử 24 câu, 18 câu trả đúng có dẫn nguồn, 6 câu sai hoặc bịa.** (75.0% ·
ghi lại đầy đủ + bảng chi tiết từng case tại `eval/run_results.md`, mục
"CP3 — Số đo … OFFLINE").

### 2.2. Lượt chạy LIVE — SỐ NỘP CP3

**Đã chạy — 2026-09-17T16:02:17.** Trước khi chạy: generate lại toàn bộ bộ
câu hỏi Day 1 + Day 2 bằng LLM thật (`regenerate:true`, xem §0), dựng lại
`eval/cp3_testset.json` khớp `question_id` mới, rồi chạy
`python3 eval/cp3_benchmark.py`. Số dưới đây copy nguyên văn từ
`eval/run_results.md` (mục "CP3 — Số đo … — 2026-09-17T16:02:17"), không làm
tròn, không chỉnh sửa:

**Thử 24 câu, 21 câu trả đúng có dẫn nguồn, 3 câu sai hoặc bịa.**

| Chỉ số | Giá trị |
|---|---|
| Thử bao nhiêu câu | 24 |
| Trả đúng có dẫn nguồn | 21 (87.5%) |
| Sai hoặc bịa | 3 (0 case bịa mã trích dẫn — cả 3 case trượt đều do lệch `verdict_label`, không có mã `[Txx-NNN]` bịa) |
| Riêng nhóm tự luận có AI chấm thật (`qtype=text`) | 13/16 đạt |
| Chế độ AI (`GET /api/health`) | `live` — `provider=openai`, `model=gpt-4o-mini` |
| Thời điểm chạy | 2026-09-17T16:02:17 |

3 case trượt (chi tiết + phân tích nguyên nhân ở `eval/run_results.md`):
- `CP3-013` (kỳ vọng `mot_phan`, AI trả `dung`) — câu hỏi trích dẫn mã
  `[T01-004]`, nhưng nội dung transcript dưới mã này chỉ là một dòng tiêu đề
  ngắn ("Bên trong LLM: cơ chế vận hành"), gần như không có nội dung thực chất
  để đối chiếu — model có khả năng đã dùng kiến thức nền của nó thay vì chỉ
  dựa vào ngữ cảnh mỏng được cấp, nên chấm "đúng" rộng rãi hơn kỳ vọng.
- `CP3-023`, `CP3-024` (kỳ vọng `ngoai_nguon_du_lieu`, AI trả `khong_du_thong_tin`)
  — cả hai case đưa câu trả lời hoàn toàn lạc đề (đi uống cà phê, xem đá banh).
  Model nhận ra đúng là câu trả lời không liên quan tới câu hỏi, nhưng gán
  nhãn `khong_du_thong_tin` thay vì `ngoai_nguon_du_lieu` — cho thấy ranh giới
  giữa hai nhãn này (thiếu thông tin vs. lạc nguồn dữ liệu) chưa được model
  phân biệt rạch ròi như kỳ vọng của thiết kế. Đáng chú ý: không case nào bịa
  mã trích dẫn — lớp "trung thực với nguồn" (`validation.invalid_codes`) hoạt
  động đúng ở toàn bộ 24/24 case.

So với lượt OFFLINE (mock, 75.0%) ở §2.1, lượt LIVE đạt cao hơn (87.5%) —
điều này hợp lý vì LLM thật (gpt-4o-mini) chấm ngữ nghĩa tốt hơn heuristic so
khớp từ khoá của mock, nhưng LIVE mới là số phản ánh đúng hành vi thật của
sản phẩm và có 3 case lệch nhãn cần lưu ý ở trên.

## 3. Lệnh chạy từ đầu đến cuối (tái lập cho người khác trong nhóm)

```bash
# 1) Cài dependency (một lần)
cd codebase/backend
pip3 install -r requirements.txt

# 2) (Bắt buộc cho video CP3) điền API key thật vào .env
#    mở codebase/backend/.env, điền một dòng, ví dụ:
#    OPENROUTER_API_KEY=sk-or-...

# 3) Chạy server (từ codebase/backend/)
python3 -m uvicorn api:app --port 8000
# server phục vụ luôn UI tại http://127.0.0.1:8000/

# 3b) Xác nhận LIVE (mở terminal khác)
curl http://127.0.0.1:8000/api/health
# kỳ vọng: {"status":"ok","mode":"live","provider":"...","model":"..."}

# 4) (Tuỳ chọn — UI đã tự làm khi bấm nút Generate) sinh lại quiz bằng tay:
curl -X POST http://127.0.0.1:8000/api/ingest  -H 'Content-Type: application/json' -d '{"day":1}'
curl -X POST http://127.0.0.1:8000/api/generate -H 'Content-Type: application/json' -d '{"day":1,"regenerate":true}'

# 5) Quay video theo kịch bản ở §1 (mở http://127.0.0.1:8000/ trên trình duyệt)

# 6) Chạy số đo CP3 (từ thư mục gốc repo, SAU khi server LIVE đang chạy)
cd ../..
python3 eval/cp3_benchmark.py
# in ra bảng chi tiết 24 case + dòng "Thử N câu, X câu trả đúng có dẫn nguồn, Y câu sai hoặc bịa"
# và tự append kết quả (không xoá nội dung cũ) vào eval/run_results.md
```

## 4. Checklist trước khi quay

- [ ] Đã điền API key thật vào `codebase/backend/.env` (không commit file này).
- [ ] Đã restart server sau khi điền key.
- [ ] `curl http://127.0.0.1:8000/api/health` trả `"mode":"live"`.
- [ ] Badge trên UI hiện **"● LIVE — ..."** màu xanh lá (không còn màu cam OFFLINE).
- [ ] Đã bấm "✨ Generate câu hỏi" cho ngày sẽ demo — số câu hiện ra là số
      thật LLM vừa sinh (không phải số cũ từ lần chạy offline trước đó).
- [ ] Đã thử trước 1 lần luồng đầy đủ (upload → generate → quiz → 1 câu MCQ →
      1 câu tự luận → summary) để chắc không lỗi giữa chừng khi quay thật.
- [ ] Sau khi quay xong: chạy `python3 eval/cp3_benchmark.py` ở chế độ LIVE,
      copy số thật vào bảng ở §2.2 của file này.
