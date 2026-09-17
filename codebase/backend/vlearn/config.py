"""Cấu hình đường dẫn + lựa chọn nhà cung cấp LLM cho vlearn.

Mọi module khác trong package `vlearn` import các hằng số từ đây thay vì tự
tính đường dẫn — tránh lặp code và tránh lệch đường dẫn giữa các module.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Đường dẫn gốc
# ---------------------------------------------------------------------------
# File này nằm tại: <repo_root>/codebase/backend/vlearn/config.py
# => đi lên 3 cấp (vlearn -> backend -> codebase) là ra repo root.
VLEARN_DIR = Path(__file__).resolve().parent
BACKEND_DIR = VLEARN_DIR.parent
CODEBASE_DIR = BACKEND_DIR.parent
REPO_ROOT = CODEBASE_DIR.parent

DATA_DIR = REPO_ROOT / "data"
SLIDES_DIR = DATA_DIR / "slides"

OUTPUT_DIR = REPO_ROOT / "output"
TRANSCRIPT_DIR = OUTPUT_DIR / "transcript"
TRANSCRIPT_INDEX_FILE = TRANSCRIPT_DIR / "index.json"

DB_PATH = OUTPUT_DIR / "quiz.db"

PROMPTS_DIR = VLEARN_DIR / "prompts"

INDEX_HTML_PATH = CODEBASE_DIR / "index.html"

GOLDEN_SET_PATH = REPO_ROOT / "eval" / "golden_set.json"
RUN_RESULTS_PATH = REPO_ROOT / "eval" / "run_results.md"


def ensure_output_dirs() -> None:
    """Tạo sẵn các thư mục output cần thiết (idempotent)."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Lựa chọn nhà cung cấp LLM (provider) + chế độ offline
# ---------------------------------------------------------------------------
# Thứ tự ưu tiên đọc API key khi không ép buộc bằng VLEARN_PROVIDER:
#   OpenRouter -> OpenAI -> Anthropic -> Gemini
# (giống thứ tự khuyến nghị trong .env.example của starter kit gốc)
PROVIDER_ENV_KEYS: dict[str, str] = {
    "openrouter": "OPENROUTER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
}

# Model mặc định gợi ý cho từng provider khi generate quiz / chấm bài.
DEFAULT_MODEL_BY_PROVIDER: dict[str, str] = {
    "openrouter": "openrouter/auto",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "gemini": "gemini-2.0-flash",
}


@dataclass(frozen=True)
class LLMSettings:
    """Kết quả resolve provider: đang chạy live hay offline (mock)."""

    mode: str  # "live" | "offline"
    provider_name: str | None  # None khi offline
    model: str | None  # None khi offline


def _has_value(env_key: str) -> bool:
    value = os.getenv(env_key, "")
    return bool(value and value.strip())


def resolve_llm_settings() -> LLMSettings:
    """Quyết định chạy live LLM hay offline (mock), dựa trên biến môi trường.

    Quy tắc:
    - Nếu `VLEARN_OFFLINE=1` (hoặc "true") -> LUÔN offline, bất kể có key hay không.
      Dùng để demo/dev/test không tốn tiền / không cần mạng.
    - Nếu `VLEARN_PROVIDER` được set (openai|openrouter|anthropic|gemini) -> dùng
      đúng provider đó, yêu cầu key tương ứng phải có, nếu không sẽ báo lỗi rõ ràng
      khi thực sự gọi LLM (llm.py xử lý fallback về offline nếu thiếu key).
    - Ngược lại: tự dò theo thứ tự ưu tiên PROVIDER_ENV_KEYS, provider nào có
      key không rỗng đầu tiên thì dùng provider đó.
    - Nếu không tìm thấy key nào -> offline.
    """
    offline_flag = os.getenv("VLEARN_OFFLINE", "").strip().lower() in {"1", "true", "yes"}
    if offline_flag:
        return LLMSettings(mode="offline", provider_name=None, model=None)

    forced_provider = os.getenv("VLEARN_PROVIDER", "").strip().lower() or None
    if forced_provider:
        if forced_provider not in PROVIDER_ENV_KEYS:
            raise ValueError(
                f"VLEARN_PROVIDER='{forced_provider}' không hợp lệ. "
                f"Chỉ chấp nhận: {', '.join(PROVIDER_ENV_KEYS)}."
            )
        if _has_value(PROVIDER_ENV_KEYS[forced_provider]):
            model = os.getenv("VLEARN_MODEL", "").strip() or DEFAULT_MODEL_BY_PROVIDER[forced_provider]
            return LLMSettings(mode="live", provider_name=forced_provider, model=model)
        # Ép provider nhưng thiếu key -> rơi về offline thay vì crash, để demo vẫn chạy được.
        return LLMSettings(mode="offline", provider_name=None, model=None)

    for provider_name, env_key in PROVIDER_ENV_KEYS.items():
        if _has_value(env_key):
            model = os.getenv("VLEARN_MODEL", "").strip() or DEFAULT_MODEL_BY_PROVIDER[provider_name]
            return LLMSettings(mode="live", provider_name=provider_name, model=model)

    return LLMSettings(mode="offline", provider_name=None, model=None)
