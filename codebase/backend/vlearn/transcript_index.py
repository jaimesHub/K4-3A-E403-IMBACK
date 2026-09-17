"""Load transcript của một Day thành index tra cứu mã [Txx-NNN] -> nội dung.

Đây là lớp "trung thực với nguồn" của toàn bộ hệ thống: mọi mã trích dẫn mà
generator.py / grader.py nhận được từ LLM (hoặc từ mock offline) đều phải đi
qua `validate_codes()` ở đây trước khi được chấp nhận lưu vào DB / trả về UI.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from vlearn import config
from vlearn.errors import VlearnError

CODE_RE = re.compile(r"\[T\d{2}-\d{3}\]")
TOKEN_RE = re.compile(r"[a-zA-ZÀ-ỹà-ỹ0-9]+")


def parse_transcript_text(text: str) -> tuple[dict[str, str], list[str], list[str]]:
    """Parse nội dung một file transcript .md thành (code -> nội dung, thứ tự mã, mã lặp).

    Hỗ trợ nội dung trải nhiều dòng cho một mã: nội dung của mã X là toàn bộ
    text từ ngay sau '[Txx-NNN]' cho tới trước mã tiếp theo (hoặc hết file).
    """
    matches = list(CODE_RE.finditer(text))
    code_map: dict[str, str] = {}
    order: list[str] = []
    duplicates: list[str] = []

    for i, match in enumerate(matches):
        code = match.group(0)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        # Bỏ heading markdown '## Slide N' còn sót lại nếu đoạn kế tiếp dính liền.
        content = re.sub(r"\n##\s.*$", "", content, flags=re.DOTALL).strip()
        if code in code_map:
            duplicates.append(code)
        else:
            order.append(code)
        code_map[code] = content

    return code_map, order, duplicates


@dataclass
class TranscriptIndex:
    day: int
    code_prefix: str
    file_path: Path
    code_map: dict[str, str] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Tra cứu
    # ------------------------------------------------------------------
    def exists(self, code: str) -> bool:
        return code in self.code_map

    def get(self, code: str) -> str | None:
        return self.code_map.get(code)

    def all_codes(self) -> list[str]:
        return list(self.order)

    def as_context_block(self, codes: list[str] | None = None) -> str:
        """Dựng khối text 'mã: nội dung' để nhét vào prompt LLM."""
        target_codes = codes if codes is not None else self.order
        lines = [f"{code} {self.code_map[code]}" for code in target_codes if code in self.code_map]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Validate — lớp "trung thực với nguồn" bắt buộc
    # ------------------------------------------------------------------
    def validate_codes(self, text: str) -> tuple[list[str], list[str]]:
        """Trích mọi mã [Txx-NNN] xuất hiện trong `text`, tách thành
        (danh sách mã hợp lệ - tồn tại thật, danh sách mã KHÔNG tồn tại)."""
        found = CODE_RE.findall(text or "")
        valid: list[str] = []
        invalid: list[str] = []
        seen: set[str] = set()
        for code in found:
            if code in seen:
                continue
            seen.add(code)
            if self.exists(code):
                valid.append(code)
            else:
                invalid.append(code)
        return valid, invalid

    # ------------------------------------------------------------------
    # Retrieval đơn giản (BM25-lite, không cần vector DB)
    # ------------------------------------------------------------------
    def search(self, query: str, top_k: int = 3) -> list[tuple[str, str, float]]:
        """Trả về top-k (code, text, score) liên quan nhất tới `query`.

        BM25-lite: TF*IDF đơn giản trên tập đoạn của transcript hiện tại,
        đủ dùng cho một transcript vài chục-vài trăm đoạn, không cần vector DB.
        """
        query_terms = [t.lower() for t in TOKEN_RE.findall(query)]
        if not query_terms or not self.order:
            return []

        doc_tokens: dict[str, list[str]] = {
            code: [t.lower() for t in TOKEN_RE.findall(self.code_map[code])] for code in self.order
        }
        n_docs = len(doc_tokens)
        avg_len = sum(len(toks) for toks in doc_tokens.values()) / max(n_docs, 1)

        df = Counter()
        for toks in doc_tokens.values():
            for term in set(toks):
                if term in query_terms:
                    df[term] += 1

        k1, b = 1.5, 0.75
        scores: list[tuple[str, str, float]] = []
        for code in self.order:
            toks = doc_tokens[code]
            if not toks:
                continue
            tf = Counter(toks)
            doc_len = len(toks)
            score = 0.0
            for term in query_terms:
                if tf[term] == 0:
                    continue
                idf = math.log(1 + (n_docs - df[term] + 0.5) / (df[term] + 0.5))
                freq = tf[term]
                score += idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avg_len))
            if score > 0:
                scores.append((code, self.code_map[code], score))

        scores.sort(key=lambda item: item[2], reverse=True)
        return scores[:top_k]

    # ------------------------------------------------------------------
    # Loader
    # ------------------------------------------------------------------
    @classmethod
    def load(cls, day: int) -> "TranscriptIndex":
        raw_index: dict[str, Any] = {}
        if config.TRANSCRIPT_INDEX_FILE.exists():
            try:
                raw_index = json.loads(config.TRANSCRIPT_INDEX_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                raw_index = {}

        entry = raw_index.get(str(day))
        if entry and entry.get("transcript_file"):
            file_path = config.REPO_ROOT / entry["transcript_file"]
        else:
            # Fallback: đoán theo quy ước tên file ngay cả khi chưa có index.json
            file_path = config.TRANSCRIPT_DIR / f"transcript-{day:02d}-clean.md"

        if not file_path.exists():
            raise VlearnError(
                f"Chưa có transcript cho Day {day} (tìm tại '{file_path}'). "
                f"Hãy chạy ingest trước: `python vlearn_cli.py ingest --day {day}`."
            )

        text = file_path.read_text(encoding="utf-8")
        code_map, order, duplicates = parse_transcript_text(text)
        if duplicates:
            print(f"[vlearn.transcript_index] Cảnh báo: mã trích dẫn lặp trong {file_path.name}: {duplicates}")
        if not order:
            raise VlearnError(
                f"File transcript '{file_path.name}' không chứa mã [Txx-NNN] nào hợp lệ."
            )

        prefix = order[0].split("-")[0].strip("[")
        return cls(day=day, code_prefix=prefix, file_path=file_path, code_map=code_map, order=order)

    @classmethod
    def from_file(cls, file_path: str | Path, *, day: int | None = None) -> "TranscriptIndex":
        """Load transcript từ một đường dẫn file bất kỳ (không theo quy ước output/transcript/).

        Dùng cho `run_quiz_eval.py`: transcript gốc của khoá học (vd transcript-04-clean.md)
        không nằm trong repo này và được người dùng trỏ tới qua đường dẫn tuỳ ý.
        """
        path = Path(file_path)
        if not path.exists():
            raise VlearnError(f"Không tìm thấy file transcript: '{path}'.")
        text = path.read_text(encoding="utf-8")
        code_map, order, duplicates = parse_transcript_text(text)
        if duplicates:
            print(f"[vlearn.transcript_index] Cảnh báo: mã trích dẫn lặp trong {path.name}: {duplicates}")
        if not order:
            raise VlearnError(f"File transcript '{path.name}' không chứa mã [Txx-NNN] nào hợp lệ.")
        prefix = order[0].split("-")[0].strip("[")
        return cls(day=day if day is not None else -1, code_prefix=prefix, file_path=path, code_map=code_map, order=order)
