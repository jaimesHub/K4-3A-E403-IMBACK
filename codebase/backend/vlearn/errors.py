"""Lớp lỗi nghiệp vụ dùng chung cho package vlearn.

Dùng `VlearnError` cho mọi lỗi có thể đoán trước và cần thông báo rõ ràng bằng
tiếng Việt cho người dùng (CLI/API) — phân biệt với lỗi hệ thống bất ngờ
(traceback Python thông thường).
"""
from __future__ import annotations


class VlearnError(Exception):
    """Lỗi nghiệp vụ của vlearn — message luôn là câu tiếng Việt rõ ràng,
    có thể hiển thị thẳng cho người dùng cuối (CLI hoặc HTTP response)."""
