# vlearn backend — "Học từ lỗi trước" (D2)

Backend + AI cho quiz sinh từ slide bài giảng: import slide → trích xuất
transcript có mã đoạn `[Txx-NNN]` → LLM sinh câu hỏi/đáp án/giải thích/trích
dẫn → lưu SQLite → UI làm quiz → chấm bài (MCQ deterministic, tự luận có
LLM) → tổng kết.

Package sống tại `codebase/backend/vlearn/` — **tách biệt hoàn toàn** với
phần helpdesk agent có sẵn (`agent.py`, `chat.py`, `tools/`, `helpdesk_data/`,
`company_policy/`). Chỉ tái sử dụng `providers/` (gọi LLM đa nhà cung cấp) và
`env_loader.py` (đọc `.env`) của starter kit gốc.

## 0. Nguyên tắc cốt lõi: trung thực với nguồn

Mọi mã `[Txx-NNN]` mà hệ thống (LLM hoặc mock offline) trả ra đều bị chạy qua
`TranscriptIndex.validate_codes()` trước khi lưu DB / trả về UI. Nếu phát
hiện mã KHÔNG tồn tại thật trong transcript, hệ thống **không im lặng bỏ
qua** — nó strip mã đó và **hạ verdict về `ngoai_nguon_du_lieu`**. Lớp chốt
chặn này nằm ở `grader._finalize_grade()` (dùng chung cho mọi đường chấm tự
luận) và `generator._validate_question_shape()` (dùng khi generate câu hỏi,
có retry cho câu lỗi ở chế độ live).

## 1. Kiến trúc

```
codebase/backend/
├── api.py                 # FastAPI — HTTP API, phục vụ luôn codebase/index.html tại "/"
├── vlearn_cli.py           # CLI — demo/test không cần UI
├── run_quiz_eval.py         # chạy eval/golden_set.json qua grader.py
├── requirements.txt         # + pypdf, fastapi, uvicorn (đã thêm)
├── .env.example              # + biến env mới của vlearn (đã thêm)
└── vlearn/
    ├── config.py            # đường dẫn (repo root, data/slides, output/...) + chọn provider/offline
    ├── errors.py             # VlearnError — lỗi nghiệp vụ, message tiếng Việt rõ ràng
    ├── ingest.py              # PDF slide -> output/transcript/transcript-<XX>-clean.md + index.json
    ├── transcript_index.py     # load transcript 1 day -> {code: text}; exists/get/search/validate_codes
    ├── db.py                   # SQLite output/quiz.db (questions, attempts) + export CSV/MD
    ├── llm.py                   # factory chọn provider (tái dùng providers/), gọi JSON completion
    ├── generator.py              # pipeline generate quiz (chọn đoạn -> LLM/mock -> validate -> retry -> lưu)
    ├── grader.py                  # MCQ deterministic (không LLM) + tự luận (LLM hoặc mock)
    └── prompts/
        ├── generate_quiz.md        # system prompt sinh câu hỏi
        ├── grade_text.md            # system prompt chấm tự luận
        └── explain_answer.md         # quy tắc cấu trúc giải thích dùng chung (không gọi LLM riêng)
```

Đường dẫn dữ liệu (tính từ repo root, không phụ thuộc cwd khi chạy):

| Việc gì | Ở đâu |
|---|---|
| Slide PDF import vào | `data/slides/d<N>-*.pdf` (vd `d1-slide-hackathon.pdf` -> Day 1) |
| Transcript sinh ra | `output/transcript/transcript-<XX>-clean.md` + `output/transcript/index.json` |
| Database quiz | `output/quiz.db` (bảng `questions`, `attempts`) |
| Export xem bằng mắt | `output/quiz_day<N>.csv`, `output/quiz_day<N>.md` |

Quy ước mã trích dẫn: **Day N → prefix `T` + 2 chữ số của N** (Day 1 →
`T01`, Day 12 → `T12`), số đoạn `NNN` tăng dần từ `001` trong phạm vi một
Day, vd `[T01-007]`.

## 2. Chế độ LIVE vs OFFLINE (mock)

`vlearn/config.py::resolve_llm_settings()` tự quyết định:

- `VLEARN_OFFLINE=1` → luôn OFFLINE, bất kể có key hay không (dùng cho demo/dev/test không tốn tiền).
- `VLEARN_PROVIDER=openai|openrouter|anthropic|gemini` → ép provider đó (yêu cầu key tương ứng có giá trị, nếu thiếu thì fallback về OFFLINE thay vì crash).
- Mặc định: tự dò key theo thứ tự `OPENROUTER_API_KEY → OPENAI_API_KEY → ANTHROPIC_API_KEY → GEMINI_API_KEY`, key nào không rỗng đầu tiên thì dùng provider đó.
- Không có key nào → OFFLINE.

**Ở trạng thái repo hiện tại, `.env` không có key nào (tất cả rỗng) → hệ
thống LUÔN chạy OFFLINE.** Chế độ OFFLINE dùng mock **deterministic dựng từ
chính transcript thật** (mã trích dẫn thật, không gọi mạng):

- `generate` OFFLINE: chọn đoạn transcript trải đều, dựng câu MCQ (đáp án +
  3 phương án nhiễu lấy từ các đoạn khác) và câu tự luận (đáp án mẫu = trích
  nguyên văn đoạn nguồn).
- `grade` (tự luận) OFFLINE: heuristic so khớp từ khoá giữa câu trả lời và
  đoạn transcript liên quan (không phải đánh giá ngữ nghĩa đầy đủ như LLM
  thật), có phát hiện đơn giản dấu hiệu prompt-injection.
- `grade` (MCQ): **luôn luôn deterministic, không bao giờ gọi LLM** — dù
  live hay offline — chỉ so `correct_key`.

Để bật LIVE: điền một trong các key trong `.env` (copy từ `.env.example`),
ví dụ `OPENROUTER_API_KEY=...`, rồi chạy lại — log khởi động sẽ in rõ
`[vlearn.llm] Chế độ LIVE — provider=...`.

## 3. Cách chạy

```bash
cd codebase/backend
pip install -r requirements.txt   # thêm pypdf, fastapi, uvicorn nếu chưa có

# 1) Trích xuất transcript từ slide cho Day 1
python vlearn_cli.py ingest --day 1

# 2) Generate bộ câu hỏi (mặc định 10 câu, tỉ lệ mcq 40%)
python vlearn_cli.py generate --day 1 --n 10

# 3) Xem lại (có đáp án) để review
python vlearn_cli.py show --day 1

# 4) Chấm thử một câu
python vlearn_cli.py grade --question-id <id> --answer "câu trả lời của bạn"

# 5) Chạy API (mặc định cổng 8000), phục vụ luôn codebase/index.html tại "/"
python vlearn_cli.py serve
# hoặc: python api.py
```

Người dùng có transcript thật (không cần sinh từ slide): thả file
`transcript-<XX>-clean.md` (đúng format `[Txx-NNN] nội dung`) vào
`output/transcript/` trước, rồi chạy `ingest --day N` — hệ thống thấy file
đã có sẽ **không ghi đè**, chỉ đọc lại để cập nhật `index.json`.

## 4. Bảng API endpoint

Base URL mặc định: `http://localhost:8000`. CORS mở cho `localhost`/`127.0.0.1` (mọi cổng).

| Method | Path | Mô tả |
|---|---|---|
| GET | `/api/health` | Trạng thái server: mode live/offline, provider, model |
| GET | `/api/days` | Danh sách Day: có slide/transcript/quiz chưa, số câu |
| POST | `/api/upload` | multipart `file` (.pdf) → lưu vào `data/slides/`, trả `{filename, day, message}` (`day` suy ra từ tên file, `null` nếu không khớp quy ước) |
| POST | `/api/ingest` | `{day}` → trích xuất transcript, trả số đoạn + đường dẫn |
| POST | `/api/generate` | `{day, num_questions?, mcq_ratio?, regenerate?}` → generate + lưu DB |
| GET | `/api/quiz/{day}` | Câu hỏi cho UI — **không lộ** `answer`/`explain`/`correct_key` |
| POST | `/api/answer` | `{question_id, user_answer}` → chấm (tự route MCQ/text theo qtype) |
| GET | `/api/summary/{day}` | Tổng kết: đúng/tổng, chi tiết từng câu, trích dẫn |
| POST | `/api/submit` | `{day, attempt_id?}` → alias của `/api/summary/{day}` (POST cho tiện frontend) |
| GET | `/api/transcript/{day}/{code}` | Tra nội dung 1 mã đoạn (code có/không có ngoặc `[...]` đều được) |
| GET | `/` | Phục vụ tĩnh `codebase/index.html` (không sửa nội dung file) |

### Ví dụ request/response

**`GET /api/health`**
```json
{"status": "ok", "mode": "offline", "provider": null, "model": null}
```

**`GET /api/days`**
```json
[
  {"day": 1, "has_slide": true, "slide_file": "d1-slide-hackathon.pdf",
   "has_transcript": true, "transcript_file": "output/transcript/transcript-01-clean.md",
   "num_segments": 37, "has_quiz": true, "num_questions": 6},
  {"day": 2, "has_slide": true, "slide_file": "d2-slide-hackathon.pdf",
   "has_transcript": false, "transcript_file": null, "num_segments": null,
   "has_quiz": false, "num_questions": 0}
]
```

**`POST /api/ingest`** — request `{"day": 1}` → response
```json
{"day": 1, "skipped_existing": false,
 "message": "Đã sinh transcript 'transcript-01-clean.md' với 37 đoạn mã [T01-NNN].",
 "transcript_file": "output/transcript/transcript-01-clean.md", "code_prefix": "T01",
 "num_segments": 37, "source_slide": "data/slides/d1-slide-hackathon.pdf",
 "ingested_at": "2026-09-17T15:07:17"}
```

**`POST /api/generate`** — request `{"day": 1, "num_questions": 6}` → response
```json
{"day": 1, "mode": "offline", "requested": 6, "generated": 6,
 "dropped_reference_codes": [], "warnings": [], "removed_existing": 0,
 "question_ids": ["834d6f4a...", "..."],
 "csv_path": "output/quiz_day1.csv", "md_path": "output/quiz_day1.md"}
```

**`GET /api/quiz/1`** (rút gọn)
```json
[
  {"id": "834d6f4a...", "day": 1, "qtype": "mcq",
   "question": "Theo bài giảng Day 1, nội dung nào sau đây mô tả ĐÚNG nhất phần được trích tại [T01-001]?",
   "options": ["Lịch sử AI 70 năm", "AI & LLM Foundation Bạn đang dùng AI mỗi ngày...", "...", "..."]},
  {"id": "06084f50...", "day": 1, "qtype": "text",
   "question": "Hãy trình bày lại bằng lời của bạn nội dung được giảng ở Day 1 (...):",
   "options": null}
]
```

**`POST /api/answer`** — request `{"question_id": "834d6f4a...", "user_answer": "B"}` → response
```json
{"verdict_label": "dung", "is_correct": true,
 "explanation": "Đúng. Đáp án đúng là B — \"AI & LLM Foundation...\". Đáp án đúng là phương án B, trích trực tiếp từ [T01-001] trong transcript.",
 "reference_code": ["[T01-001]"],
 "reference_quote": ["AI & LLM Foundation Bạn đang dùng AI mỗi ngày — nhưng thực sự bên trong nó đang làm gì?"],
 "reference_url": ["output/transcript/transcript-01-clean.md#T01-001"],
 "model_used": null,
 "validation": {"invalid_codes": []}}
```

**`GET /api/summary/1`** (rút gọn — mỗi `items[i]` là 1 câu, `answered: false` nếu chưa làm)
```json
{"day": 1, "total_questions": 6, "answered": 2, "correct": 1, "score_percent": 16.7,
 "items": [{"question_id": "...", "question": "...", "qtype": "mcq",
            "reference_code": "[T01-001]", "reference_url": "...", "answered": true,
            "verdict_label": "dung", "is_correct": true, "explanation": "...",
            "attempt_reference_code": ["[T01-001]"], "attempt_reference_quote": ["..."],
            "user_answer": "B"}, "..."]}
```

**`GET /api/transcript/1/T01-001`**
```json
{"day": 1, "code": "[T01-001]", "text": "AI & LLM Foundation Bạn đang dùng AI mỗi ngày — nhưng thực sự bên trong nó đang làm gì?"}
```
Không tìm thấy mã → HTTP 404 `{"error": "Không tìm thấy mã '[T99-999]' trong transcript Day 1."}`

Lỗi nghiệp vụ (`VlearnError`, vd thiếu slide, thiếu transcript, day không
hợp lệ...) → HTTP 400 `{"error": "<thông báo tiếng Việt rõ ràng>"}`.

## 5. Chạy eval (golden set)

```bash
python run_quiz_eval.py --transcript /đường/dẫn/tới/transcript-04-clean.md
# hoặc:
export VLEARN_EVAL_TRANSCRIPT=/đường/dẫn/tới/transcript-04-clean.md
python run_quiz_eval.py
```

`transcript-04-clean.md` (nguồn sự thật của `eval/golden_set.json`) là dữ
liệu thật của khoá học và **KHÔNG được commit vào repo** (xem
`CHECKLIST.md`) — vì vậy nó **không có sẵn** trong thư mục này. Script BẮT
BUỘC nhận đường dẫn qua `--transcript` hoặc biến môi trường
`VLEARN_EVAL_TRANSCRIPT`; nếu thiếu, script in cảnh báo rõ ràng bằng tiếng
Việt và `exit(1)` — **không tự bịa transcript hay bịa kết quả eval**.

Mỗi case được chấm qua `grader.grade_open_answer()` — cùng "động cơ chấm"
(prompt `grade_text.md` hoặc mock offline) mà sản phẩm dùng để chấm bài tự
luận thật; khác biệt duy nhất là eval không biết trước `reference_code`, hệ
thống tự tìm đoạn liên quan bằng `TranscriptIndex.search()` (BM25-lite).

Script tự động kiểm tra **chính xác bằng code**:
- Điều kiện 1 — `verdict_label` khớp kỳ vọng (so khớp enum, không mơ hồ).
- Điều kiện 4 — mọi mã `[Txx-NNN]` AI trích ra tồn tại thật + khớp đúng
  `reference_code` kỳ vọng (case `n/a` thì không được trích mã nào). Đây là
  phép grep ngược lại transcript, không thể bịa.

Và **heuristic** (so khớp từ khoá, có giới hạn) cho:
- Điều kiện 2 — giải thích có phủ hết `explanation_must_cover`.
- Điều kiện 3 — giải thích không chứa ý nào trong `must_not_contain`.

> Heuristic 2/3 KHÔNG thay thế được việc người đọc lại — đúng tinh thần cột
> "người chấm tick từng ý" trong bảng gốc của `eval/run_results.md`. Với các
> case biên (đặc biệt case TRƯỢT chỉ vì điều kiện 2/3), nên đọc lại
> `explanation` thật trong output trước khi kết luận cuối cùng.

Script in bảng kết quả + tỷ lệ % + kiểm tra 3 điều kiện quality bar (≥80%,
100% nhóm an toàn GS-002/006/007/008/009/025, 0 case bịa mã), rồi **append**
(không xoá nội dung cũ) một section mới vào `eval/run_results.md`.

## 6. Trạng thái đã tự test (offline, xem báo cáo đầy đủ trong PR/chat)

Đã chạy thật: `ingest --day 1`, `ingest --day 2`, `generate --day 1/2`,
`show`, `grade` (MCQ đúng/sai, tự luận đúng/quá ngắn/prompt-injection),
`serve` + curl toàn bộ endpoint, `regenerate`. Đã grep ngược **100%** mã
trích dẫn trong `output/quiz.db` (bảng `questions` + `attempts`) về đúng
transcript tương ứng — **0 mã bịa**.

`run_quiz_eval.py` CHƯA chạy được với dữ liệu thật vì `transcript-04-clean.md`
không có trong repo (đúng chủ đích bảo mật dữ liệu) — đã verify nhánh lỗi
"thiếu transcript" in đúng thông báo tiếng Việt và `exit(1)`, không đụng vào
`eval/run_results.md`.

## 7. Bật LIVE LLM

1. Copy `.env.example` → `.env` (đã có sẵn ở `codebase/backend/.env`).
2. Điền MỘT trong các key: `OPENROUTER_API_KEY` (khuyến nghị),
   `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, hoặc `GEMINI_API_KEY`.
3. (Tuỳ chọn) đặt `VLEARN_PROVIDER` để ép chọn provider cụ thể, `VLEARN_MODEL`
   để ép model cụ thể — không đặt thì hệ thống tự dò/dùng model mặc định.
4. Chạy lại — log sẽ in `[vlearn.llm] Chế độ LIVE — provider='...', model='...'`.
5. Muốn ép offline dù có key (test nhanh, tiết kiệm tiền): `VLEARN_OFFLINE=1`.
