# RUNBOOK — Hướng dẫn chạy app và test CP3

> Tài liệu này giúp các thành viên trong nhóm: (A) chạy app vlearn từ đầu đến cuối, (B) chạy benchmark đo độ chính xác theo mốc CP3. Toàn bộ lệnh và số liệu đã được xác minh trên môi trường thực tế.

---

## Phần A — Chạy ứng dụng

### 1. Yêu cầu môi trường

| Thành phần | Yêu cầu |
|---|---|
| Python | 3.8+ |
| Pip | có sẵn với Python |
| Port | 8000 (chưa bị chiếm) |
| Trình duyệt | Hỗ trợ mới (Chrome, Firefox, Safari) |
| Thư mục gốc | `/Users/jaimes/Working/AI20K-IV/K4-3A-E403-IMBACK` |

### 2. Cài đặt dependencies

```bash
cd /Users/jaimes/Working/AI20K-IV/K4-3A-E403-IMBACK/codebase/backend
pip install -r requirements.txt
```

**Dependencies chính:** `pypdf`, `fastapi`, `uvicorn`, `openai` (bắt buộc cho chế độ LIVE).

Nếu thiếu `openai`, server sẽ báo lỗi:
```
RuntimeError: Install live provider dependency first: pip install openai
```

### 3. Cấu hình API key (để chạy LIVE)

**LIVE mode** yêu cầu 1 trong 4 key sau:

- `OPENAI_API_KEY` (được khuyến nghị) — được sử dụng mặc định
- `OPENROUTER_API_KEY` (rẻ, đa model)
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`

Mở file `codebase/backend/.env` (nếu không có, copy từ `.env.example`), rồi điền 1 key. Ví dụ:

```bash
# codebase/backend/.env
OPENAI_API_KEY=sk-...
```

**Lưu ý:** File `.env` bị `.gitignore`, không commit.

Nếu `.env` **không có** key nào → server chạy **OFFLINE** (chế độ mock, không gọi mạng).

### 4. Khởi động server

```bash
cd /Users/jaimes/Working/AI20K-IV/K4-3A-E403-IMBACK/codebase/backend
python3 -m uvicorn api:app --port 8000
```

Khi server khởi động xong, sẽ in:
```
INFO:     Application startup complete
```

Server sẽ phục vụ UI tại `http://127.0.0.1:8000/`.

### 5. Xác nhận chế độ LIVE

Mở terminal khác, chạy:

```bash
curl http://127.0.0.1:8000/api/health
```

**Nếu có API key:**
```json
{"status":"ok","mode":"live","provider":"openai","model":"gpt-4o-mini"}
```

**Nếu không có API key:**
```json
{"status":"ok","mode":"offline","provider":null,"model":null}
```

Trên UI (góc phải trên cùng), sẽ hiển thị badge:
- **LIVE mode:** `● LIVE — openai · gpt-4o-mini` (màu xanh lá)
- **OFFLINE mode:** `● OFFLINE (mock — chưa có API key)` (màu cam)

### 6. Luồng sử dụng app (6 màn)

| Bước | Màn hình | Việc làm |
|---|---|---|
| 1 | Import tài liệu | Chọn/kéo thả file PDF slide, bấm "Tiếp theo →" |
| 2 | Nhập ngày | Gõ số ngày (1, 2, ...), bấm "✨ Generate câu hỏi" |
| 3 | Thông báo xong | Chờ quá trình xong, xem số câu MCQ/tự luận thực sinh |
| 4 | Quiz | Làm lần lượt các câu (MCQ chấm tự động, tự luận gửi cho AI chấm) |
| 5 | Phân tích từng câu | Xem giải thích, trích dẫn từ transcript (mã `[Txx-NNN]`) |
| 6 | Tổng kết | Xem điểm số, danh sách câu đúng/sai |

### 7. Bảng endpoint API

Base URL: `http://127.0.0.1:8000`

| Method | Path | Mô tả |
|---|---|---|
| GET | `/api/health` | Kiểm tra mode (live/offline), provider, model |
| GET | `/api/days` | Danh sách Day: có slide/transcript/quiz không, số câu |
| POST | `/api/upload` | Upload PDF (multipart file) vào `data/slides/` |
| POST | `/api/ingest` | `{day}` — trích xuất transcript từ PDF |
| POST | `/api/generate` | `{day, num_questions?, mcq_ratio?, regenerate?}` — sinh câu hỏi |
| GET | `/api/quiz/{day}` | Lấy danh sách câu hỏi (không lộ đáp án) |
| POST | `/api/answer` | `{question_id, user_answer}` — chấm câu, trả verdict + giải thích |
| GET | `/api/summary/{day}` | Tổng kết: điểm, chi tiết từng câu, trích dẫn |
| GET | `/api/transcript/{day}/{code}` | Tra nội dung 1 mã đoạn (vd: `T01-001`) |
| GET | `/` | Phục vụ UI tĩnh (`codebase/index.html`) |

### 8. Chạy từ command line (CLI)

Thay vì dùng UI, có thể dùng:

```bash
cd /Users/jaimes/Working/AI20K-IV/K4-3A-E403-IMBACK/codebase/backend

# Trích transcript từ slide Day 1
python3 vlearn_cli.py ingest --day 1

# Sinh bộ 10 câu hỏi cho Day 1
python3 vlearn_cli.py generate --day 1 --n 10

# Xem lại câu hỏi (có đáp án)
python3 vlearn_cli.py show --day 1

# Chấm thử một câu (ID lấy từ output/quiz.db)
python3 vlearn_cli.py grade --question-id <id_hex> --answer "câu trả lời của bạn"

# Chạy server (giống lệnh ở §4)
python3 vlearn_cli.py serve
```

### 9. Thư mục dữ liệu

| Dữ liệu | Ở đâu |
|---|---|
| Slide PDF | `data/slides/d<N>-*.pdf` (vd: `d1-slide-hackathon.pdf` → Day 1) |
| Transcript | `output/transcript/transcript-<XX>-clean.md` (mã `[T01-NNN]`, `[T02-NNN]`, ...) |
| Database quiz | `output/quiz.db` (bảng `questions`, `attempts`) |
| Export xem | `output/quiz_day<N>.csv`, `output/quiz_day<N>.md` |

---

## Phần B — Test & Đo theo CP3

### 1. CP3 yêu cầu gì

| Yêu cầu | Chi tiết |
|---|---|
| Video | 30 giây quay màn hình, từ mở app đến thấy AI trả kết quả có trích dẫn |
| **Bắt buộc** | ≥ 1 lời gọi AI **chạy thật** (mode LIVE, không mock) — thường là câu tự luận được AI chấm |
| Số đo | Bộ 24 case từ `eval/cp3_testset.json`, tính % case đúng |
| Chuẩn đạt | (1) `verdict_label` API trả phải khớp kỳ vọng, **VÀ** (2) không có mã trích dẫn bịa |

### 2. Cách chạy benchmark CP3

**Điều kiện:** Server đang chạy ở chế độ **LIVE** (có API key, `curl /api/health` trả `"mode":"live"`).

Mở terminal mới, chạy từ gốc repo:

```bash
cd /Users/jaimes/Working/AI20K-IV/K4-3A-E403-IMBACK
python3 eval/cp3_benchmark.py
```

Script sẽ:
1. Gửi HTTP request tới `http://127.0.0.1:8000/api/answer` cho mỗi case
2. Kiểm tra `verdict_label` + mã trích dẫn
3. In bảng chi tiết 24 case
4. Tự động append kết quả vào `eval/run_results.md`

### 3. Bộ test CP3

- **Tệp:** `eval/cp3_testset.json`
- **Số case:** 24 (yêu cầu ≥ 20)
- **Thành phần:**
  - 8 case MCQ (4 đúng, 4 sai)
  - 16 case tự luận (gồm: đúng, một phần, sai, quá mơ hồ, ngoài phạm vi, lạc đề)
- **Phân bố kỳ vọng:** dung 8 · sai 7 · mot_phan 3 · khong_du_thong_tin 2 · ngoai_pham_vi 2 · ngoai_nguon_du_lieu 2
- **Bảo vệ:** Có case chống prompt-injection (`CP3-021`)

### 4. Chuẩn đạt 1 case

Một case được tính **ĐẠT** khi:

1. `verdict_label` (nhãn do API trả về) **khớp** `expected_verdict` (nhãn trong testset)
2. **Không có mã** `[Txx-NNN]` **bịa** — mọi mã AI trích đều tồn tại thật trong transcript

Nếu cả 2 điều kiện thỏa → ĐẠT. Nếu lệch bất kỳ điều kiện nào → TRƯỢT.

### 5. Số đo mới nhất (LIVE — 2026-09-17T16:02:17)

**Môi trường:**
- Mode: **LIVE** (provider=`openai`, model=`gpt-4o-mini`)
- Bộ câu hỏi Day 1 + Day 2 được generate lại bằng LLM thật (không dùng mock)

**Kết quả:**

| Chỉ số | Giá trị |
|---|---|
| Thử bao nhiêu câu | 24 |
| **Đạt** (verdict đúng + không bịa mã) | **21** (87.5%) |
| Trượt | 3 (0 case bịa mã) |
| Nhóm tự luận AI chấm (`qtype=text`) | 13/16 đạt |

**So sánh:** Chế độ OFFLINE (mock, không gọi mạng) đạt 75.0% (18/24). LIVE cao hơn do LLM thật chấm ngữ nghĩa tốt hơn heuristic so khớp từ khóa.

### 6. Phân tích 3 case trượt

| Case | Nhóm | Kỳ vọng | AI trả | Nguyên nhân |
|---|---|---|---|---|
| CP3-013 | Tự luận | `mot_phan` | `dung` | Transcript dưới mã `[T01-004]` chỉ là tiêu đề ngắn, model dùng kiến thức nền thay vì chỉ ngữ cảnh mỏng, nên chấm rộng rãi hơn kỳ vọng |
| CP3-023 | Tự luận | `ngoai_nguon_du_lieu` | `khong_du_thong_tin` | Câu trả lời hoàn toàn lạc đề (uống cà phê), model nhận ra không liên quan nhưng gán nhãn `khong_du_thong_tin` thay vì `ngoai_nguon_du_lieu` — ranh giới 2 nhãn chưa rạch ròi |
| CP3-024 | Tự luận | `ngoai_nguon_du_lieu` | `khong_du_thong_tin` | Giống CP3-023 — lạc đề (xem đá banh), nhược điểm phân loại nhãn |

**Quan trọng:** Cả 3 case đều **không bịa mã trích dẫn** — lớp bảo vệ chống tạo mã giả hoạt động đúng 24/24 case.

### 7. Script eval thứ hai (chưa chạy được)

Có script `codebase/backend/run_quiz_eval.py` chấm bộ `eval/golden_set.json` (25 case khác):

```bash
# Cần transcript-04-clean.md (không có trong repo vì bảo mật dữ liệu)
python3 codebase/backend/run_quiz_eval.py --transcript /đường/dẫn/tới/transcript-04-clean.md
```

Script sẽ **không chạy** nếu thiếu file `transcript-04-clean.md` — nó in cảnh báo tiếng Việt rõ ràng và `exit(1)`, không tự bịa kết quả.

---

## Xử lý sự cố

### Lỗi: "RuntimeError: Install live provider dependency first"

**Nguyên nhân:** Thiếu SDK `openai`.

**Cách khắc:**
```bash
pip install openai
```

### Lỗi: `curl /api/health` trả `"mode":"offline"` dù đã điền key

**Nguyên nhân:**
1. Quên khởi động lại server sau khi điền key
2. `.env` chưa lưu hoặc lưu sai vị trí

**Cách khắc:**
```bash
# Kiểm tra .env có key không
cat codebase/backend/.env

# Khởi động lại server
python3 -m uvicorn api:app --port 8000
```

### Lỗi: Port 8000 đang bị dùng

**Cách khắc:**
```bash
# Tìm process dùng port 8000
lsof -i :8000

# Hoặc chạy server ở port khác
python3 -m uvicorn api:app --port 8001
```

### Lỗi: Chưa ingest/generate mà đã click vào quiz

**Hành động:** UI sẽ báo "Chưa có câu hỏi cho Day này". Bấm "← Quay lại" rồi:
1. Upload slide
2. Bấm "✨ Generate câu hỏi"
3. Chờ xong, bấm "🚀 Bắt đầu làm quiz →"

### Lỗi: Server không chạy nhưng cố mở UI

**Dấu hiệu:** Trình duyệt báo không thể kết nối `http://127.0.0.1:8000`.

**Cách khắc:** Mở terminal, chạy server (§4).

---

## Tái lập nhanh (từ đầu đến có số đo)

```bash
# 1. Vào thư mục backend
cd /Users/jaimes/Working/AI20K-IV/K4-3A-E403-IMBACK/codebase/backend

# 2. Cài dependencies (nếu chưa)
pip install -r requirements.txt

# 3. Điền API key (VÍ DỤ)
echo "OPENAI_API_KEY=sk-..." > .env

# 4. Khởi động server (chạy trên terminal 1)
python3 -m uvicorn api:app --port 8000
# Chờ tới "Application startup complete"

# 5. Kiểm tra LIVE (trên terminal 2)
curl http://127.0.0.1:8000/api/health
# Kỳ vọng: {"status":"ok","mode":"live",...}

# 6. Trích transcript + Sinh câu hỏi (nếu chưa có)
python3 vlearn_cli.py ingest --day 1
python3 vlearn_cli.py generate --day 1 --n 24

# 7. Chạy benchmark CP3 (từ gốc repo, terminal 2)
cd /Users/jaimes/Working/AI20K-IV/K4-3A-E403-IMBACK
python3 eval/cp3_benchmark.py
# Kết quả tự append vào eval/run_results.md

# 8. Xem kết quả
tail -50 eval/run_results.md
```

---

## Mục lục

- **Phần A — Chạy ứng dụng**
  1. Yêu cầu môi trường
  2. Cài đặt dependencies
  3. Cấu hình API key (LIVE)
  4. Khởi động server
  5. Xác nhận chế độ LIVE
  6. Luồng sử dụng app (6 màn)
  7. Bảng endpoint API
  8. Chạy từ CLI
  9. Thư mục dữ liệu

- **Phần B — Test & Đo theo CP3**
  1. CP3 yêu cầu gì
  2. Cách chạy benchmark
  3. Bộ test CP3 (24 case)
  4. Chuẩn đạt 1 case
  5. Số đo mới nhất (87.5%, 21/24)
  6. Phân tích 3 case trượt
  7. Script eval thứ hai (chưa chạy được)

- **Xử lý sự cố** (5 tình huống)
- **Tái lập nhanh** (8 bước copy-paste)
