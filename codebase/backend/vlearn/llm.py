"""Factory chọn provider LLM (tái sử dụng providers/ có sẵn) + gọi JSON completion.

Chế độ offline (mock) KHÔNG nằm ở đây — nó nằm ở generator.py/grader.py vì cần
truy cập transcript index để dựng output deterministic hợp lệ (mã thật). Module
này chỉ lo phần "live": chọn provider, gọi API, parse JSON strict trả về.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any

from vlearn import config
from vlearn.errors import VlearnError

# Đảm bảo import được providers/ và env_loader.py ở codebase/backend/, bất kể
# script entry point (api.py / vlearn_cli.py / run_quiz_eval.py) được chạy từ
# thư mục nào.
_BACKEND_DIR_STR = str(config.BACKEND_DIR)
if _BACKEND_DIR_STR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR_STR)

from env_loader import load_lab_env  # noqa: E402  (import sau khi chỉnh sys.path)
from providers import make_provider  # noqa: E402

load_lab_env(config.BACKEND_DIR)

SETTINGS = config.resolve_llm_settings()

if SETTINGS.mode == "live":
    print(
        f"[vlearn.llm] Chế độ LIVE — provider='{SETTINGS.provider_name}', model='{SETTINGS.model}'."
    )
else:
    print(
        "[vlearn.llm] Chế độ OFFLINE (mock) — không có API key hợp lệ hoặc VLEARN_OFFLINE=1. "
        "Generate/chấm bài sẽ dùng dữ liệu dựng sẵn từ chính transcript thật (mã trích dẫn thật, "
        "không gọi mạng)."
    )


def is_offline() -> bool:
    return SETTINGS.mode == "offline"


def _extract_json_object(raw_text: str) -> dict[str, Any]:
    """Parse JSON từ text trả về của LLM, chịu được rác bao quanh (```json ... ```)."""
    text = raw_text.strip()
    # Bỏ code fence kiểu ```json ... ``` nếu có.
    fence_match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, flags=re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Fallback: cắt từ dấu '{' đầu tiên đến dấu '}' cuối cùng.
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass
    raise VlearnError(f"LLM trả về không phải JSON hợp lệ. Nội dung thô: {raw_text[:500]!r}")


def call_llm_json(system_prompt: str, user_prompt: str, *, temperature: float = 0.2) -> dict[str, Any]:
    """Gọi LLM live và parse JSON strict. Chỉ dùng khi SETTINGS.mode == 'live'."""
    if SETTINGS.mode != "live":
        raise VlearnError("call_llm_json() được gọi khi đang ở chế độ offline — đây là lỗi logic nội bộ.")

    provider = make_provider(SETTINGS.provider_name)
    response = provider.complete(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        tools=None,
        model=SETTINGS.model,
        temperature=temperature,
    )
    if not response.text:
        raise VlearnError("LLM không trả về nội dung text nào (response rỗng).")
    return _extract_json_object(response.text)


def load_prompt(name: str) -> str:
    """Đọc một file prompt .md trong vlearn/prompts/."""
    path = config.PROMPTS_DIR / name
    if not path.exists():
        raise VlearnError(f"Không tìm thấy file prompt '{name}' trong {config.PROMPTS_DIR}")
    return path.read_text(encoding="utf-8")
