"""vlearn — backend + AI cho sản phẩm "Học từ lỗi trước" (D2 VLearn quiz).

Package này tách biệt hoàn toàn với phần helpdesk agent có sẵn trong
`codebase/backend/` (agent.py, chat.py, tools/, helpdesk_data/, company_policy/).
Nó chỉ TÁI SỬ DỤNG lớp `providers/` (chuẩn hoá gọi LLM đa nhà cung cấp) và
`env_loader.py` (đọc file .env) đã có sẵn ở thư mục cha.
"""
