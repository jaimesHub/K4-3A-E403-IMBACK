# CP5 — Cần bổ sung gì trước khi làm slide

> Viết trên branch `khanhdq/cp5`, dựa trên `khanhdq/cp4` (spec.md đã chốt) — chưa merge vào `main`.
> Nguyên tắc theo handbook trang 08: *"Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính."* Mọi ô "thiếu" dưới đây khai thẳng, không đoán số để lấp.

---

## 1. Bảng 6 slide × trạng thái sẵn sàng

| # | Slide | Trạng thái | Thiếu gì cụ thể | Ai phải cung cấp |
|---|---|---|---|---|
| 1 | User & Job | 🟡 Thiếu một phần (đã có dữ liệu thật, chưa đủ chuẩn) | Đã có khảo sát thật `fix-gaps/1-Survey.csv` (n=5, 16/09/2026): 5/5 xác nhận gặp khó khăn với workflow lý thuyết→ví dụ→bài tập; 3/5 nói "tự làm bài tập, mắc lỗi rồi được giải thích" giúp hiểu khái niệm khó nhất; 4 quote nguyên văn có nội dung. Còn thiếu: (a) chưa đủ ≥5 quote theo yêu cầu `spec.md §1` (đang có 4); (b) form ẩn danh, không có trường "người nói" (chỉ có Dấu thời gian) nên không đạt chuẩn nguồn đầy đủ; (c) n=5 rất nhỏ, chưa đại diện toàn khoá — xem đánh giá chi tiết ở `fix-gaps/1-Survey-DANHGIA.md`. | Cả nhóm — nếu muốn đạt 🟢 cần thêm ≥1 quote nữa + khảo sát rộng hơn n=5 để có số liệu đại diện |
| 2 | Vì sao chọn tính năng này | 🟡 Thiếu một phần (đã lấp 2/12 ô bằng số/ước lượng có nguồn) | Có 3 ứng viên + lý do loại (thật, trong `spec.md §2`). Đã lấp thêm bằng số có nguồn cho **2 ô** của ứng viên đã chọn: tần suất = 1 lượt quiz/buổi (đếm từ `output/quiz.db`, Day 1+2 = 10 câu/buổi), tốn-gì-mỗi-lần = **30,0 phút trung bình (n=5 người, ngày 18/09/2026, khoảng 20–40, tách nhóm: đã học AI20K n=2 → 30,0 phút; chưa học n=3 → 30,0 phút — không chênh lệch về thời gian) — số đo bấm giờ thật** từ `fix-gaps/3-BANG-DO-THOI-GIAN.md`, không phải ước lượng từ độ dài. Còn thiếu **10/12 ô**: cột "bao nhiêu người" cho cả 3 ứng viên, và tần suất + chi phí cho 2 ứng viên bị loại — **khảo sát `fix-gaps/1-Survey.csv` không lấp được các ô này**, form không hỏi tần suất pain, không hỏi chi phí/thời gian mỗi lần, và không hỏi riêng cho từng ứng viên. Rủi ro bất đối xứng (chỉ ứng viên chọn có số, 2 ứng viên loại trống) đã được đánh giá và xử lý bằng cách nói thẳng trên slide/spec — xem `fix-gaps/2-Impact-DANHGIA.md` | Cả nhóm — cần khảo sát riêng có câu hỏi về tần suất/chi phí (đặc biệt cho 2 ứng viên loại), và thêm quote cho slide 1 |
| 3 | Giải pháp & demo live | 🟢 Sẵn sàng | Lát cắt 1 câu có sẵn (`spec.md §4`), automation + cost-of-error có sẵn (`spec.md §4` mục Automation), case chuẩn (`CP3-009..012` dung) và case chỗ khó (`CP3-021` prompt-injection, `CP3-022` hành chính) đều đã đo thật và ĐẠT. Chỉ cần dựng lại server + tập demo trước khi lên sân khấu | Người demo (cần chốt ở §8 phân công — hiện chưa có ai nhận việc "demo") |
| 4 | Kết quả đo | 🔴 Thiếu số chính | Quality bar đã chốt (`spec.md §7`), nhưng **golden set 25 case (`eval/golden_set.json`) chưa chạy được lần nào** — thiếu đúng file `transcript-04-clean.md`. Có số thật thay thế: 87.5% (21/24) trên bộ `eval/cp3_testset.json` — **là bộ khác golden set**, phải nói rõ trên slide, không được ngầm hiểu là golden set | Người giữ `transcript-04-clean.md` (dữ liệu khoá học, không có trong repo) — cần xin/cấp file rồi chạy `codebase/backend/run_quiz_eval.py --transcript <path>` |
| 5 | User thật nói gì | 🟢 Sẵn sàng (validation thật đã xong; còn lại là thực hiện thay đổi trong code) | Đã chạy xong vòng dùng thử thật: **5/5 người ngoài nhóm, 2/2 người từ CP1** (Nguyễn Phương Nam, Lại Bá Quân), thu **5 quote nguyên văn** — bảng nhật ký đầy đủ ở `validation/README.md`. Đã chọn 2 quote mạnh nhất lên slide (Lại Bá Quân — loading, Lê Hoàng Anh — ngôn ngữ hàn lâm) và 4 thay đổi **đã quyết định** từ feedback (Case #2, #3, #4, #5). **Còn thiếu:** cả 4 thay đổi này **CHƯA được thực hiện trong code** (đã xác nhận bằng `git status`, `grade_text.md` chưa bị sửa) — cần làm trước demo (xem slide 6); ngày chạy buổi (16–18/09/2026) đã được người chạy buổi xác nhận. Rủi ro "thủng cả hai đường" ở mục 3 **không còn đúng nữa** — đường validation đã thông | Cả nhóm — ưu tiên còn lại là: thực hiện ≥1 trong 4 thay đổi đã quyết định trước demo |
| 6 | Nếu có thêm 1 tuần | 🟢 Sẵn sàng | Không cần dữ liệu mới — chỉ cần trỏ đúng về 3 failure đã biết thật: `CP3-013` (ngữ cảnh mỏng), `CP3-023`/`CP3-024` (nhầm nhãn `khong_du_thong_tin` vs `ngoai_nguon_du_lieu`), và việc chạy golden set còn treo. Bài học lớn nhất có thể rút từ `eval/EVAL_REPORT_v1.md §5`. ⚠️ Lưu ý: nội dung slide 6 hiện tại (việc 3) vẫn viết "hoàn thành vòng dùng thử... để đủ điều kiện checklist CP5" như validation chưa xong — **đã lỗi thời so với thực tế** (validation đã xong, xem slide 5), nhưng nằm ngoài phạm vi được phép sửa của lượt cập nhật này | Người viết slide (dùng dữ liệu có sẵn, không cần thu thập thêm) — cần cập nhật lại việc 3 của slide 6 ở một lượt sau |

**Tóm tắt (đã cập nhật sau khi chạy xong vòng dùng thử thật Phần B, 5/5 người):** 3/6 slide sẵn sàng (3, 5, 6); 2/6 thiếu một phần (1, 2); 1/6 thiếu bằng chứng chính (4). Slide 5 chuyển từ 🔴 "thủng cả hai đường" sang 🟢 nhờ vòng dùng thử thật đã chạy xong (5/5 người, 2/2 từ CP1, 5 quote) — chi tiết ở dòng slide 5 và mục 3 bên dưới; điểm còn lại là thực hiện thay đổi trong code + xác nhận ngày, không còn là "chưa có bằng chứng nào". Slide 1 chuyển từ 🔴 sang 🟡 nhờ có khảo sát n=5 thật, nhưng chưa lên 🟢 vì chưa đủ ≥5 quote và thiếu trường nguồn "người nói" — xem mục 6 và `fix-gaps/1-Survey-DANHGIA.md`. Slide 2 vẫn ở 🟡 nhưng đã lấp được 2/12 ô của bảng impact bằng số có nguồn (tần suất 1 quiz/buổi từ `output/quiz.db` + chi phí 30,0 phút trung bình từ **số đo bấm giờ thật Phần A** `fix-gaps/3-BANG-DO-THOI-GIAN.md` — n=5 người, tách nhóm: 30,0 phút cho cả nhóm đã học AI20K n=2 lẫn nhóm chưa học n=3 — không chênh lệch về thời gian, giới hạn n nhỏ) — 10/12 ô còn lại (cột "bao nhiêu người" cho cả 3 ứng viên + toàn bộ số liệu 2 ứng viên loại) vẫn để trống vì không có nguồn dữ liệu, không phải vì giấu — xem `fix-gaps/2-Impact-DANHGIA.md`.

---

## 2. Bảng checklist CP5 (4 mục) × trạng thái thật

| # | Mục | Yêu cầu | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 1 | Slide 6 trang (PDF) + video demo dự phòng | Xuất PDF, quay sẵn phần demo phòng mạng hỏng | 🟡 Draft nội dung xong (`CP5_SLIDES_DRAFT.md`), **chưa có file PDF, chưa quay video** | Cần: (a) dựng slide thật từ draft, xuất PDF; (b) quay video demo case chuẩn + case chỗ khó theo kịch bản ở slide 3, dùng làm phương án dự phòng |
| 2 | ≥5 người ngoài nhóm dùng thử, trong đó ≥2 người đã khai từ CP1 | 5 người thật, 2 người có nguồn gốc từ CP1 | 🟢 **5/5** — đã chạy xong vòng dùng thử thật: Nguyễn Phương Nam, Lại Bá Quân (2 người từ CP1), Trần Minh Tuấn, Lê Hoàng Anh, Phạm Quỳnh Nga (tuyển thêm). Danh sách + phân loại rõ willing user vs tuyển thêm ở `validation/README.md` | Không còn việc gì gấp ở mục này — không còn việc gì tồn đọng ở mục này |
| 3 | Bảng nhật ký + quote nguyên văn trong `validation/` | Ghi ai thử, giao task gì, kẹt ở đâu, quote gốc | 🟢 Đã điền đầy đủ bảng nhật ký thật + 5 quote nguyên văn (chép đúng, giữ cả lỗi chính tả) ở `validation/README.md` | Ngày thử trong bảng đã được xác nhận (16–18/09/2026); dòng Changelog đã được cập nhật phù hợp |
| 4 | ≥1 thay đổi ghi vào §9 Changelog · `reflection/` mỗi người 1 file | Đổi ≥1 điều theo feedback thật + 4 file reflection cá nhân | 🟡 Đã ghi **4 thay đổi** vào `spec.md §9` (Case #2, #3, #4, #5, vượt yêu cầu ≥1), nhưng **CẢ 4 ĐỀU CHƯA ĐƯỢC THỰC HIỆN TRONG CODE** — đã kiểm tra `git status`, `grade_text.md` (Case #4) chưa hề bị sửa; ghi rõ trạng thái "đã quyết định — chưa thực hiện", không ghi như đã làm xong. `reflection/` nay đã có đủ **4/4 file cá nhân** (`duong-quoc-khanh.md`, `luu-manh-hung.md`, `nguyen-cong-minh.md`, `nguyen-ngoc-minh.md`) với phần bối cảnh chung điền sẵn, nhưng **phần cảm nhận cá nhân của từng người vẫn để trống** (`🔲 [CHÍNH CHỦ ĐIỀN]`, chờ chính người đó viết) | Cần thực hiện ≥1 trong 4 thay đổi đã quyết định trước demo (ưu tiên Case #4 vì đã có prompt file cụ thể để sửa); từng thành viên tự điền phần cảm nhận cá nhân trong file reflection của mình — khung đã có, nội dung cảm nhận thật vẫn thiếu |

**Tóm tắt:** 2.5/4 mục checklist CP5 đã hoàn thành thật (mục 2, 3 xong; mục 4 mới xong nửa — đã quyết định 4 thay đổi nhưng chưa thực hiện trong code, khung 4 file reflection cá nhân đã tạo nhưng phần cảm nhận thật của từng người vẫn để trống); mục 1 vẫn chỉ có draft nội dung (chưa xuất PDF/quay video). Khác biệt lớn nhất so với trạng thái trước: mục 2, 3 không còn phụ thuộc dây chuyền vào "có được 5 người dùng thử thật" nữa — việc đó đã xong.

---

## 3. Rủi ro riêng: Slide 5 — ĐÃ CẬP NHẬT, đường validation nay đã thông

> ⚠️ Mục này mô tả rủi ro cũ ("thủng cả hai đường") — **nay không còn đúng nữa**, giữ lại có gạch để đối chiếu, kèm trạng thái mới ngay dưới.

Đề bài cho phép "nhóm không làm validation thì thay bằng kết quả đo trên golden set: đạt/không đạt quality bar và vì sao". Trước đây **cả hai đường cùng thủng**:

- ~~Đường 1 (validation thật): không có `validation/`, chưa có ai dùng thử → không có quote nguyên văn.~~ **→ Đã xử lý xong.** Đã chạy vòng dùng thử thật 5/5 người ngoài nhóm (2/2 từ CP1), thu 5 quote nguyên văn — `validation/README.md`.
- Đường 2 (dự phòng bằng golden set): `eval/golden_set.json` (25 case) **vẫn chưa chạy được lần nào**, vì thiếu file `transcript-04-clean.md` → vẫn không có tỉ lệ đạt/không đạt để trình bày (không nằm trong phạm vi sửa của lượt cập nhật này — xem slide 4).

**Trạng thái mới:** slide 5 không còn phụ thuộc vào golden set nữa — đường validation đã đủ bằng chứng để lên slide (5 người, 2 nguồn CP1, 5 quote, ≥1 thay đổi đã quyết định từ feedback theo đúng yêu cầu R6). Rủi ro còn lại **không phải "không có gì để trình bày"** nữa, mà là hai điểm nhỏ hơn:

1. **Thay đổi đã quyết định nhưng chưa thực hiện trong code** — nếu ban giám khảo hỏi "đã sửa chưa", câu trả lời trung thực hiện tại là "chưa, mới quyết định" (đã xác nhận bằng `git status`). Cần thực hiện ≥1 thay đổi trước demo để câu trả lời mạnh hơn, hoặc chuẩn bị tinh thần khai thẳng nếu chưa kịp.

**Khuyến nghị xử lý theo mức độ dễ (đã cập nhật):**
1. Xác nhận lại ngày thu dữ liệu thật ở `validation/README.md` và dòng Changelog tương ứng ở `spec.md §9` — rẻ, chỉ cần người đã chạy buổi xác nhận.
2. Thực hiện ≥1 trong 4 thay đổi đã quyết định (ưu tiên Case #4 — sửa `grade_text.md`, đã có sẵn hướng làm) trước demo.
3. Golden set (`transcript-04-clean.md`) vẫn là việc riêng của slide 4, không còn là "nửa rủi ro của slide 5" nữa vì slide 5 đã có đường validation đứng vững một mình.

---

## 4. Thứ tự ưu tiên việc cần làm gấp

| Ưu tiên | Việc | Vì sao gấp | Ước lượng ai làm |
|---|---|---|---|
| 🔴 1 | Xin/cấp file `transcript-04-clean.md`, chạy golden set 25 case | Mở khoá số đo chính thức cho slide 4; chỉ thiếu đúng 1 file, script đã sẵn sàng (`codebase/backend/run_quiz_eval.py`). *(Không còn là "một nửa rủi ro của slide 5" nữa — slide 5 đã có đường validation đứng vững riêng, xem mục 3)* | 1 người giữ dữ liệu khoá học cấp file + 1 người trong nhóm chạy script, có thể xong trong một buổi |
| ✅ 2 | ~~Chốt danh sách 5 người dùng thử ngoài nhóm (2 người đã khai từ CP1), bắt đầu vòng dùng thử~~ | **ĐÃ XONG.** 5/5 người ngoài nhóm, 2/2 từ CP1, đã thực sự dùng thử và có 5 quote nguyên văn — `validation/README.md`. Điều kiện bắt buộc của checklist mục 2, 3 đã đủ | — |
| 🔴 2b | Thực hiện ≥1 trong 4 thay đổi đã quyết định từ feedback (ưu tiên Case #4 — sửa `codebase/backend/vlearn/prompts/grade_text.md`) trước demo | Hiện tại 4 thay đổi mới ở mức "đã quyết định", `git status` xác nhận code chưa đổi — nếu không làm trước demo, mục 4 checklist CP5 vẫn chỉ được nửa điểm và slide 5/slide 6 kém thuyết phục hơn | Người phụ trách code (chưa phân công cụ thể — xem `spec.md §8`) |
| 🟡 3 | Khảo sát/mining bổ sung cho slide 1–2 | **Slide 1 đã có một phần** nhờ `fix-gaps/1-Survey.csv` (n=5, 16/09/2026) — còn thiếu ≥1 quote nữa + trường "người nói" để đạt chuẩn `spec.md §1`. **Slide 2 đã lấp một phần** (2/12 ô, bằng số: tần suất từ `output/quiz.db` + chi phí từ **số đo bấm giờ thật Phần A** `fix-gaps/3-BANG-DO-THOI-GIAN.md` — đã xong ngày 18/09/2026, n=5 người, 30,0 phút trung bình, tách nhóm) — vẫn thiếu cột "bao nhiêu người" (cả 3 ứng viên) và toàn bộ số liệu 2 ứng viên loại; không chặn checklist CP5 bắt buộc nhưng để trống thì bảng impact vẫn phải giữ khung `⚠️ chưa có số` / `🔲 CẦN BỔ SUNG` ở các ô đó | Cả nhóm — mở rộng khảo sát n>5 kèm câu hỏi tần suất/chi phí riêng cho từng ứng viên (đặc biệt 2 ứng viên loại), và thêm quote cho slide 1 để đạt chuẩn |
| ✅ 4 | ~~Ghi ≥1 thay đổi thật vào `spec.md §9 Changelog` dựa trên feedback từ vòng dùng thử~~ | **ĐÃ XONG (vượt yêu cầu):** 4 thay đổi đã ghi vào `spec.md §9`, trỏ đúng Case #2/#3/#4/#5. Còn lại chỉ là thực hiện trong code (xem 🔴2b) | — |
| 🟡 5 | Mỗi thành viên viết `reflection/<ten>.md` | Khung 4 file cá nhân **đã được tạo** (bối cảnh chung điền sẵn), nhưng phần cảm nhận cá nhân của từng người vẫn để trống (`🔲 [CHÍNH CHỦ ĐIỀN]`) — cần chính chủ tự viết, không ai viết hộ | Từng thành viên tự điền phần cảm nhận trong file của mình |
| 🟢 6 | Dựng slide thật từ `CP5_SLIDES_DRAFT.md`, xuất PDF + quay video demo dự phòng | Bước cuối cùng; slide 5 đã có nội dung thật để dựng, chỉ còn chờ slide 4 (golden set) và các mục 🔴 ở trên | Người phụ trách trình bày (chưa phân công — xem `spec.md §8`) |

---

## 5. Ghi chú

- File này không sửa `spec.md`, không sửa `eval/*`, không chạy server/benchmark — chỉ tổng hợp lại đúng những gì `spec.md`, `REPORT_CP4.md`, `eval/EVAL_REPORT_v1.md`, `eval/run_results.md` đã khai, đối chiếu với 4 yêu cầu CP5.
- Vai trò từng thành viên (`spec.md §8`, `TEAMMATES.md`) đã được điền xong — các thành viên nắm được phần có tên mình trong bảng phân công.

---

## 6. Nguồn dữ liệu mới: `fix-gaps/1-Survey.csv`

- **File:** `fix-gaps/1-Survey.csv` (không sửa file gốc — dữ liệu khảo sát giữ nguyên).
- **Quy mô:** n = 5 người trả lời, thời điểm 16/09/2026 19:25–19:29 (5 lượt trong ~4 phút).
- **Dùng để:** lấp một phần "con số pain" ở slide 1 (mục 1 trên) — KHÔNG dùng được cho bảng impact ở slide 2, và KHÔNG thay thế được validation sản phẩm ở slide 5 (khảo sát này diễn ra trước khi có sản phẩm để dùng thử).
- **Giới hạn đã ghi nhận:** n=5 rất nhỏ (trình bày dạng phân số, không quy % để tránh gây ấn tượng sai về quy mô); câu hỏi "giả sử có công cụ..." là câu hỏi dẫn dắt nên 5/5 "Có" ở đó là bằng chứng yếu; form ẩn danh, chỉ có Dấu thời gian, không có tên/vai người trả lời; chỉ có 4/5 quote nguyên văn có nội dung so với yêu cầu ≥5 của `spec.md §1`.
- **Đánh giá đầy đủ (mạnh/yếu ở đâu, đối chiếu problem statement, danh sách quote):** xem `fix-gaps/1-Survey-DANHGIA.md`.
- **Khuyến nghị về `spec.md §1`:** spec.md **đã được cập nhật** ở nhánh `khanhdq/cp5` với dữ liệu khảo sát thật. Xem `fix-gaps/1-Survey-DANHGIA.md` mục 2.5 để hiểu độ khớp đầy đủ.
