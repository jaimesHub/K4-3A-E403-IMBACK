# CP5 — Cần bổ sung gì trước khi làm slide

> Viết trên branch `khanhdq/cp5`, dựa trên `khanhdq/cp4` (spec.md đã chốt) — chưa merge vào `main`.
> Nguyên tắc theo handbook trang 08: *"Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính."* Mọi ô "thiếu" dưới đây khai thẳng, không đoán số để lấp.

---

## 1. Bảng 6 slide × trạng thái sẵn sàng

| # | Slide | Trạng thái | Thiếu gì cụ thể | Ai phải cung cấp |
|---|---|---|---|---|
| 1 | User & Job | 🔴 Thiếu bằng chứng | Không có khảo sát/mining thật trong repo (đã khai từ CP4 §1) — không có n=?, không có % xác nhận pain, không có quote nguyên văn kèm nguồn. Job executor + JTBD một câu thì **có sẵn** trong `spec.md §1`, nhưng "con số pain" theo đúng yêu cầu slide 1 thì **chưa có**. | Cả nhóm — cần khảo sát tối thiểu học viên AI20K hoặc mining `tutor_turns.csv` (nếu có sẵn trong nguồn dữ liệu khoá học) để ra được con số thật trước khi lên slide |
| 2 | Vì sao chọn tính năng này | 🟡 Thiếu một phần | Có 3 ứng viên + lý do loại (thật, trong `spec.md §2`), nhưng cột số liệu (bao nhiêu người/tần suất/chi phí) của cả 3 ứng viên đều đánh dấu `⚠️ chưa có số` — chưa điền được vì phụ thuộc đúng bộ khảo sát còn thiếu ở slide 1 | Cả nhóm — cùng nguồn dữ liệu với mục Evidence ở trên |
| 3 | Giải pháp & demo live | 🟢 Sẵn sàng | Lát cắt 1 câu có sẵn (`spec.md §4`), automation + cost-of-error có sẵn (`spec.md §4` mục Automation), case chuẩn (`CP3-009..012` dung) và case chỗ khó (`CP3-021` prompt-injection, `CP3-022` hành chính) đều đã đo thật và ĐẠT. Chỉ cần dựng lại server + tập demo trước khi lên sân khấu | Người demo (cần chốt ở §8 phân công — hiện chưa có ai nhận việc "demo") |
| 4 | Kết quả đo | 🔴 Thiếu số chính | Quality bar đã chốt (`spec.md §7`), nhưng **golden set 25 case (`eval/golden_set.json`) chưa chạy được lần nào** — thiếu đúng file `transcript-04-clean.md`. Có số thật thay thế: 87.5% (21/24) trên bộ `eval/cp3_testset.json` — **là bộ khác golden set**, phải nói rõ trên slide, không được ngầm hiểu là golden set | Người giữ `transcript-04-clean.md` (dữ liệu khoá học, không có trong repo) — cần xin/cấp file rồi chạy `codebase/backend/run_quiz_eval.py --transcript <path>` |
| 5 | User thật nói gì | 🔴 Thủng cả hai đường | Không có `validation/` → không có quote user thật. Phương án dự phòng của đề bài ("thay bằng % đạt/không đạt golden set") **cũng không dùng được** vì golden set chưa chạy (xem slide 4). Đây là rủi ro lớn nhất của cả bộ slide — xem mục 3 bên dưới | Cả nhóm — cần làm xong validation (mục 2 checklist CP5) HOẶC chạy xong golden set (slide 4) trước khi có thể điền slide này bằng số/quote thật |
| 6 | Nếu có thêm 1 tuần | 🟢 Sẵn sàng | Không cần dữ liệu mới — chỉ cần trỏ đúng về 3 failure đã biết thật: `CP3-013` (ngữ cảnh mỏng), `CP3-023`/`CP3-024` (nhầm nhãn `khong_du_thong_tin` vs `ngoai_nguon_du_lieu`), và việc chạy golden set còn treo. Bài học lớn nhất có thể rút từ `eval/EVAL_REPORT_v1.md §5` | Người viết slide (dùng dữ liệu có sẵn, không cần thu thập thêm) |

**Tóm tắt:** 2/6 slide sẵn sàng (3, 6); 1/6 thiếu một phần (2); 3/6 thiếu bằng chứng chính (1, 4, 5).

---

## 2. Bảng checklist CP5 (4 mục) × trạng thái thật

| # | Mục | Yêu cầu | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 1 | Slide 6 trang (PDF) + video demo dự phòng | Xuất PDF, quay sẵn phần demo phòng mạng hỏng | 🟡 Draft nội dung xong (`CP5_SLIDES_DRAFT.md`), **chưa có file PDF, chưa quay video** | Cần: (a) dựng slide thật từ draft, xuất PDF; (b) quay video demo case chuẩn + case chỗ khó theo kịch bản ở slide 3, dùng làm phương án dự phòng |
| 2 | ≥5 người ngoài nhóm dùng thử, trong đó ≥2 người đã khai từ CP1 | 5 người thật, 2 người có nguồn gốc từ CP1 | 🔴 **0/5** — repo không có danh sách willing users nào (đã khai từ CP4 §8), không rõ có khai willing users ở CP1 hay chưa | Cần nhóm xác nhận CP1 đã khai ai chưa; nếu chưa, tìm đủ 5 người ngoài nhóm trước khi vào vòng dùng thử |
| 3 | Bảng nhật ký + quote nguyên văn trong `validation/` | Ghi ai thử, giao task gì, kẹt ở đâu, quote gốc | 🔴 Thư mục `validation/` **chưa tồn tại trước session này** — session này chỉ tạo khung `validation/README.md` (bảng trống, chưa có dữ liệu thật) | Cần người phụ trách chạy vòng dùng thử thật rồi điền bảng |
| 4 | ≥1 thay đổi ghi vào §9 Changelog · `reflection/` mỗi người 1 file | Đổi ≥1 điều theo feedback thật + 4 file reflection cá nhân | 🔴 Chưa có thay đổi nào ghi vào §9 vì chưa có feedback thật (phụ thuộc mục 2, 3); `reflection/` **chưa tồn tại trước session này** — session này chỉ tạo khung `reflection/README.md` liệt kê 4 tên, chưa có file cá nhân nào | Sau khi có feedback thật ở mục 3, mới có gì để đổi + ghi changelog; mỗi thành viên tự viết file reflection riêng |

**Tóm tắt:** 0/4 mục checklist CP5 đã hoàn thành thật; mục 1 có draft nội dung (chưa xuất PDF/quay video); mục 2, 3, 4 đều ở mức 0 vì phụ thuộc dây chuyền vào việc có được 5 người dùng thử thật.

---

## 3. Rủi ro riêng: Slide 5 thủng cả hai đường

Đề bài cho phép "nhóm không làm validation thì thay bằng kết quả đo trên golden set: đạt/không đạt quality bar và vì sao". Nhưng ở trạng thái hiện tại của repo, **cả hai đường đều thủng cùng lúc**:

- Đường 1 (validation thật): không có `validation/`, chưa có ai dùng thử → không có quote nguyên văn.
- Đường 2 (dự phòng bằng golden set): `eval/golden_set.json` (25 case) **chưa chạy được lần nào**, vì thiếu file `transcript-04-clean.md` → không có tỉ lệ đạt/không đạt để trình bày.

Hệ quả: nếu không xử lý được **ít nhất một trong hai** đường trước khi lên slide, slide 5 sẽ phải trình bày ở dạng khung chờ (đã dựng sẵn trong `CP5_SLIDES_DRAFT.md`), điều này công khai một khoảng trống lớn trước ban giám khảo. Đây là rủi ro nghiêm trọng nhất trong toàn bộ 6 slide vì đây là mục duy nhất R6 (8 điểm) cho phép về nếu không có validation — và cả hai lối thoát đều đang đóng.

**Khuyến nghị xử lý theo mức độ dễ:**
1. Chạy golden set trước (chỉ cần 1 file `transcript-04-clean.md` + 1 lệnh chạy script có sẵn) — rẻ hơn nhiều so với tổ chức vòng dùng thử.
2. Song song tổ chức vòng dùng thử thật (5 người, 2 người từ CP1) để có quote thật — vừa phục vụ slide 5 vừa là điều kiện bắt buộc của checklist mục 2, 3, 4.
3. Nếu đến hạn chỉ làm được một trong hai, ưu tiên đường golden set vì đây cũng là input bắt buộc cho slide 4 (không chỉ slide 5).

---

## 4. Thứ tự ưu tiên việc cần làm gấp

| Ưu tiên | Việc | Vì sao gấp | Ước lượng ai làm |
|---|---|---|---|
| 🔴 1 | Xin/cấp file `transcript-04-clean.md`, chạy golden set 25 case | Mở khoá đồng thời slide 4 (số đo chính thức) và một nửa rủi ro của slide 5; chỉ thiếu đúng 1 file, script đã sẵn sàng (`codebase/backend/run_quiz_eval.py`) | 1 người giữ dữ liệu khoá học cấp file + 1 người trong nhóm chạy script, có thể xong trong một buổi |
| 🔴 2 | Chốt danh sách 5 người dùng thử ngoài nhóm (2 người đã khai từ CP1), bắt đầu vòng dùng thử | Điều kiện bắt buộc của cả 3 mục còn lại trong checklist CP5 (mục 2, 3, 4) và là nguồn duy nhất còn lại cho slide 5 nếu golden set không kịp | Trưởng nhóm (Dương Quốc Khánh) điều phối, cả 4 thành viên cùng liên hệ người quen trong/ngoài khoá |
| 🟡 3 | Khảo sát/mining tối thiểu cho slide 1–2 (con số pain + bảng impact) | Không chặn checklist CP5 (không phải 1 trong 4 mục bắt buộc), nhưng nếu thiếu thì slide 1–2 phải chạy bằng khung `🔲 CẦN BỔ SUNG`, làm yếu phần mở đầu bài thuyết trình | Cả nhóm, có thể làm song song với mục 1–2 vì dùng chung nguồn người được khảo sát/dùng thử |
| 🟢 4 | Ghi ≥1 thay đổi thật vào `spec.md §9 Changelog` dựa trên feedback từ vòng dùng thử | Phụ thuộc mục 🔴2 có kết quả trước; đây là bước cuối sau khi có ít nhất 1 quote/feedback thật | Người tổng hợp validation (chưa phân công — xem `spec.md §8`) |
| 🟢 5 | Mỗi thành viên viết `reflection/<ten>.md` | Không phụ thuộc dữ liệu ngoài — làm được bất cứ lúc nào, nhưng nên làm sau khi có trải nghiệm thật từ vòng dùng thử để reflection có nội dung | Từng thành viên tự viết |
| 🟢 6 | Dựng slide thật từ `CP5_SLIDES_DRAFT.md`, xuất PDF + quay video demo dự phòng | Bước cuối cùng, nên làm sau khi các mục số liệu ở trên đã có kết quả thật để điền vào chỗ `🔲 CẦN BỔ SUNG` | Người phụ trách trình bày (chưa phân công — xem `spec.md §8`) |

---

## 5. Ghi chú

- File này không sửa `spec.md`, không sửa `eval/*`, không chạy server/benchmark — chỉ tổng hợp lại đúng những gì `spec.md`, `REPORT_CP4.md`, `eval/EVAL_REPORT_v1.md`, `eval/run_results.md` đã khai, đối chiếu với 4 yêu cầu CP5.
- Vai trò từng thành viên (`spec.md §8`, `TEAMMATES.md`) vẫn đang để trống — cần điền trước khi phân việc ở bảng ưu tiên trên có người chịu trách nhiệm cụ thể.
