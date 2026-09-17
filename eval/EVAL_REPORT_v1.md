# Báo cáo đo lường — CP3 (v1)

**Ngày 17/9/2026** · Branch: `main` · Commit thực hiện: `a2d829e` (16:03:55) · Chế độ AI: **LIVE** (provider=`openai`, model=`gpt-4o-mini`)

---

## 1. Tóm tắt kết quả

**Số đo chính thức (định dạng handbook):**

> **Thử 24 câu, 21 câu trả đúng có dẫn nguồn, 3 câu sai hoặc bịa.**

- **Tỉ lệ đạt:** 87.5% (21/24)
- **Nhóm câu tự luận (`qtype=text`):** 13/16 đạt
- **Nhóm trắc nghiệm (`qtype=mcq`):** 8/8 đạt
- **Số case phát hiện bịa mã trích dẫn:** 0/24

---

## 2. Sản phẩm & quyết định AI được đo

**Sản phẩm:** VLearn Quiz — "Học từ lỗi trước" (D2 Foundation)

**Quyết định AI đem đi đo:** 
- Đọc câu trả lời của học viên
- So sánh với nội dung transcript của bài giảng  
- Trả về nhận định về tính đúng/sai kèm giải thích + trích dẫn nguồn có mã định danh `[Txx-NNN]`
- **Tiêu chí chất lượng:** Không được phép bịa mã trích dẫn (không tồn tại trong transcript thật)

---

## 3. Phương pháp đo

### 3.1. Bộ câu thử

**Testset:** `eval/cp3_testset.json` · **24 case** · Bao gồm Day 1 (T01-xxx) và Day 2 (T02-xxx)

Thành phần:
- **8 case MCQ** (trắc nghiệm) — được chấm deterministic (so sánh key, KHÔNG gọi LLM)
- **16 case Text** (tự luận) — được chấm thực sự bằng AI (gọi LLM trên đoạn `reference` trong DB)

Phân bố `expected_verdict`:
- `dung` (đúng hoàn toàn): 8 case
- `sai` (sai hoàn toàn): 7 case  
- `mot_phan` (đúng một phần): 3 case
- `khong_du_thong_tin` (thiếu thông tin): 2 case
- `ngoai_nguon_du_lieu` (nằm ngoài transcript): 2 case
- `ngoai_pham_vi` (ngoài phạm vi): 2 case

### 3.2. Cách chạy & bằng chứng chốt chuẩn

**Chuẩn ĐẠT được chốt bằng:**

Commit `687c8b4` vào **15:48:53** (trước lượt chạy LIVE 15 phút) — chốt chuẩn trước khi biết kết quả, đúng yêu cầu handbook trang 06:

```
commit 687c8b4 (2026-09-17 15:48:53)
Author: khanhdq
Subject: chore: CP3 chuẩn đạt — 24 case + định nghĩa ĐẠT
```

Phân bố `expected_verdict` **không thay đổi** từ trước đến sau khi chạy LIVE.

**Định nghĩa ĐẠT của MỘT case:**

Một case tính **ĐẠT** khi thoả **CẢ HAI** điều kiện:
1. `verdict_label` API trả về **khớp** `expected_verdict` trong testset
2. Mọi mã `[Txx-NNN]` API trả ra đều **tồn tại thật** trong transcript — tức `validation.invalid_codes` rỗng

(Xem docstring đầu file `eval/cp3_benchmark.py` để chi tiết)

### 3.3. Chế độ & bằng chứng AI LIVE

**Xác nhận chế độ LIVE lúc chạy:**

Truy vấn `GET /api/health` trả về:
```json
{
  "status": "ok",
  "mode": "live",
  "provider": "openai",
  "model": "gpt-4o-mini"
}
```

**Quá trình chạy:**
- Server: `cd codebase/backend && python3 -m uvicorn api:app --port 8000`
- Script: `python3 eval/cp3_benchmark.py` (từ gốc repo)
- Lệnh gọi API: `POST /api/answer` với từng case trong testset
- Thời điểm hoàn tất: 2026-09-17T16:02:17
- Kết quả tự động append vào `eval/run_results.md`

---

## 4. Kết quả chi tiết

### 4.1. Bảng tổng hợp

| Chỉ số | Giá trị |
|---|---|
| Tổng case | 24 |
| Case ĐẠT | 21 |
| Case TRƯỢT | 3 |
| Tỉ lệ ĐẠT (%) | 87.5 |
| MCQ ĐẠT | 8/8 |
| Text ĐẠT | 13/16 |
| Case bịa mã trích dẫn | 0 |

### 4.2. Bảng chi tiết 24 case

| Case | Nhóm | Kỳ vọng | AI trả về | C1 khớp verdict | C2 không bịa mã | Đạt |
|---|---|---|---|---|---|---|
| CP3-001 | MCQ dung | dung | dung | ✓ | ✓ | ĐẠT |
| CP3-002 | MCQ dung | dung | dung | ✓ | ✓ | ĐẠT |
| CP3-003 | MCQ dung | dung | dung | ✓ | ✓ | ĐẠT |
| CP3-004 | MCQ dung | dung | dung | ✓ | ✓ | ĐẠT |
| CP3-005 | MCQ sai | sai | sai | ✓ | ✓ | ĐẠT |
| CP3-006 | MCQ sai | sai | sai | ✓ | ✓ | ĐẠT |
| CP3-007 | MCQ sai | sai | sai | ✓ | ✓ | ĐẠT |
| CP3-008 | MCQ sai | sai | sai | ✓ | ✓ | ĐẠT |
| CP3-009 | Text dung | dung | dung | ✓ | ✓ | ĐẠT |
| CP3-010 | Text dung | dung | dung | ✓ | ✓ | ĐẠT |
| CP3-011 | Text dung | dung | dung | ✓ | ✓ | ĐẠT |
| CP3-012 | Text dung | dung | dung | ✓ | ✓ | ĐẠT |
| CP3-013 | Text mot_phan | mot_phan | dung | ✗ | ✓ | TRƯỢT |
| CP3-014 | Text mot_phan | mot_phan | mot_phan | ✓ | ✓ | ĐẠT |
| CP3-015 | Text mot_phan | mot_phan | mot_phan | ✓ | ✓ | ĐẠT |
| CP3-016 | Text sai | sai | sai | ✓ | ✓ | ĐẠT |
| CP3-017 | Text sai | sai | sai | ✓ | ✓ | ĐẠT |
| CP3-018 | Text sai | sai | sai | ✓ | ✓ | ĐẠT |
| CP3-019 | Text khong_du_thong_tin | khong_du_thong_tin | khong_du_thong_tin | ✓ | ✓ | ĐẠT |
| CP3-020 | Text khong_du_thong_tin | khong_du_thong_tin | khong_du_thong_tin | ✓ | ✓ | ĐẠT |
| CP3-021 | Text ngoai_pham_vi | ngoai_pham_vi | ngoai_pham_vi | ✓ | ✓ | ĐẠT |
| CP3-022 | Text ngoai_pham_vi | ngoai_pham_vi | ngoai_pham_vi | ✓ | ✓ | ĐẠT |
| CP3-023 | Text ngoai_nguon_du_lieu | ngoai_nguon_du_lieu | khong_du_thong_tin | ✗ | ✓ | TRƯỢT |
| CP3-024 | Text ngoai_nguon_du_lieu | ngoai_nguon_du_lieu | khong_du_thong_tin | ✗ | ✓ | TRƯỢT |

**Ký hiệu:**
- C1 = Điều kiện 1 (khớp verdict_label)
- C2 = Điều kiện 2 (không bịa mã trích dẫn)
- ✓ = Thoả · ✗ = Vi phạm

---

## 5. Phân tích ba case trượt

### 5.1. CP3-013 — Ngữ cảnh reference quá tối giản

| Thông tin | Chi tiết |
|---|---|
| **Nhóm** | Text mot_phan |
| **Kỳ vọng** | `mot_phan` |
| **AI trả về** | `dung` |
| **Lỗi** | Lệch nhãn (C1 vi phạm) · `validation.invalid_codes` rỗng (C2 thoả) |
| **Nguyên nhân** | Mã nguồn `[T01-004]` trong DB được lưu chỉ là một dòng tiêu đề ngắn (vì `reference_quote` mà AI sinh câu đã chọn trích chỉ cái heading). Khi chấm, LLM nhận được ngữ cảnh mỏng → chấm rộng tay hơn kỳ vọng. Người làm testset soạn `expected_verdict` dựa trên TOÀN BỘ nội dung transcript gốc (với example đầy đủ), nhưng LLM grader chỉ nhận đoạn `reference` hẹp hơn. |
| **Kết luận** | Đây không phải lỗi của chuẩn hay testset, mà là hiệu ứng đã biết về hẹp ngữ cảnh (ghi chú trong `cp3_testset.json`) |

### 5.2 & 5.3. CP3-023 & CP3-024 — Nhầm lẫn hai nhãn phân loại

| Thông tin | CP3-023 | CP3-024 |
|---|---|---|
| **Nhóm** | Text ngoai_nguon_du_lieu | Text ngoai_nguon_du_lieu |
| **Kỳ vọng** | `ngoai_nguon_du_lieu` | `ngoai_nguon_du_lieu` |
| **AI trả về** | `khong_du_thong_tin` | `khong_du_thong_tin` |
| **Lỗi** | Lệch nhãn (C1 vi phạm) · Không bịa mã (C2 thoả) | Lệch nhãn (C1 vi phạm) · Không bịa mã (C2 thoả) |
| **Trường hợp** | Câu trả lời lạc đề hẳn · Model nhận ra không liên quan nhưng gán nhãn sai | Giống CP3-023 |

### 5.4. Nhận xét bắt buộc

**Lớp chống bịa trích dẫn hoạt động đúng 24/24:** Cả ba case trượt **không case nào bịa nguồn** — mã `[Txx-NNN]` AI trả ra đều tồn tại thật trong transcript.

**Lỗi tập trung duy nhất:** Model không phân biệt được ranh giới giữa hai nhãn:
- `khong_du_thong_tin` — Học viên trả lời rỗng / mơ hồ / không đủ dữ liệu để đánh giá
- `ngoai_nguon_du_lieu` — Chủ đề **hợp lệ** (liên quan tới bài học) nhưng transcript **không có căn cứ** để trả lời

Ranh giới này chưa được mô tả **đủ rõ** trong `codebase/backend/vlearn/prompts/grade_text.md`.

### 5.5. Hướng sửa

Làm rõ ranh giới hai nhãn trong system prompt, kèm ví dụ cụ thể. 

**Ước tính:** Nếu sửa xong và chạy lại bộ 24 case này (do cả lượt LIVE đầu tiên và lượt LIVE thứ hai đều xảy ra lỗi y hệt tại CP3-023 & CP3-024, nên lỗi là hệ thống, không nhiễu ngẫu nhiên), sẽ lấy lại được **2/3 case** → **23/24 (95.8%)**.

---

## 6. So sánh LIVE vs OFFLINE

| Chỉ số | OFFLINE (mock) | LIVE (gpt-4o-mini) |
|---|---|---|
| Thời điểm | 2026-09-17T15:47:31 | 2026-09-17T16:02:17 |
| Chế độ grading text | Heuristic từ khóa (`_mock_grade`) | LLM thật |
| Tổng case ĐẠT | 18/24 | 21/24 |
| Tỉ lệ (%) | 75.0 | 87.5 |
| Text ĐẠT | 10/16 | 13/16 |
| MCQ ĐẠT | 8/8 | 8/8 |
| Case bịa mã | 0 | 0 |

**Ghi chú:** Hai lượt OFFLINE (lần 1–2) kết quả y hệt (18/24); hai lượt LIVE (lần 3–4) cũng y hệt (21/24), chạy độc lập bởi hai người.

---

## 7. Khoảng trống & việc còn lại

### 7.1. Golden set chưa chạy được

**Định nghĩa chất lượng CP3 (spec.md §7)** dựa trên bộ golden set:
- **File:** `eval/golden_set.json` · 25 case
- **Chuẩn ĐẠT:** 
  - Tỉ lệ ≥ 80% (≥ 20/25 case) **VÀ**
  - 100% nhóm an toàn đạt (6 case: GS-002, 006, 007, 008, 009, 025) **VÀ**
  - 0 case bịa mã trích dẫn

**Vấn đề:** Chưa chạy được vì thiếu file `transcript-04-clean.md` (dữ liệu khoá học, không commit vào repo). Script đã sẵn sàng:
```bash
cd codebase/backend
python3 run_quiz_eval.py --transcript <đường dẫn>/transcript-04-clean.md
```

**Mối quan hệ:** Bộ 24 case CP3 ở báo cáo này **KHÁC** golden set — là bộ kiểm tra "thử bao nhiêu, đúng bao nhiêu", không thay thế golden set.

### 7.2. Ngữ cảnh reference hẹp

Ghi chú trong `cp3_testset.json` lưu ý: Khi chấm câu tự luận, grader chỉ nhận được đoạn `reference` (trích từ DB), có thể ngắn hơn nhiều so với toàn bộ đoạn transcript gốc. `expected_verdict` được soạn dựa trên TOÀN BỘ nội dung thật (theo quy tắc CP3), nên có khả năng model chấm lệch do thiếu ngữ cảnh. Đây là **một phát hiện thật** về hạn chế của hệ thống, không phải lỗi của testset.

---

## 8. Cách tái lập kết quả

### 8.1. Điều kiện tiên quyết

- `.env` phải có `OPENAI_API_KEY` (API key OpenAI hợp lệ)
- Python 3.9+
- Backend dependencies đã được cài (requirements.txt)

### 8.2. Các bước

**Bước 1: Khởi động backend server**
```bash
cd codebase/backend
python3 -m uvicorn api:app --port 8000 &
```

**Bước 2: Xác nhận server chạy ở chế độ LIVE**
```bash
curl http://127.0.0.1:8000/api/health
```

Phải trả về:
```json
{"status":"ok","mode":"live","provider":"openai","model":"gpt-4o-mini"}
```

**Bước 3: Chạy benchmark**
```bash
cd <gốc repo>
python3 eval/cp3_benchmark.py
```

**Bước 4: Kiểm tra kết quả**

Script sẽ in ra console và **tự động append vào `eval/run_results.md`**. Dòng nội dung mới sẽ nằm dưới heading "CP3 — Số đo … — [timestamp]".

---

## 9. Tài liệu tham khảo

| File | Mục đích |
|---|---|
| `eval/cp3_benchmark.py` | Script chạy test, chứa docstring định nghĩa ĐẠT |
| `eval/cp3_testset.json` | Bộ 24 case (meta + cases) |
| `eval/golden_set.json` | Bộ 25 case golden (chưa chạy được) |
| `eval/run_results.md` | Lịch sử tất cả lượt chạy |
| `codebase/backend/vlearn/prompts/grade_text.md` | System prompt chấm câu tự luận (cần cải thiện ranh giới khong_du_thong_tin vs ngoai_nguon_du_lieu) |
| `codebase/backend/run_quiz_eval.py` | Script chạy golden set (sẵn sàng, chưa sử dụng) |
| `spec.md §7` | Định nghĩa quality bar CP3 |
