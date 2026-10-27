"""Prompt construction and code extraction."""
from __future__ import annotations

import re

from .problems.base import Problem

SYSTEM_PROMPT = (
    "You are an expert Python programmer solving coding-interview problems. "
    "Reply with exactly one complete Python 3 solution inside a single ```python code block. "
    "Define the function with the exact name and signature given. Use only the standard library. "
    "Do not read input, print, or include tests. Correctness and efficiency both matter: "
    "your solution is run against hidden tests with large inputs and a time limit."
)


def build_user_prompt(p: Problem) -> str:
    return (
        f"# {p.title} ({p.difficulty})\n\n{p.prompt.strip()}\n\n"
        f"Function signature:\n```python\n{p.starter.strip()}\n```\n"
    )


_BLOCK = re.compile(r"```(?:python|py|Python)?[ \t]*\n(.*?)```", re.DOTALL)


def extract_code(text: str, entry_point: str) -> str:
    blocks = _BLOCK.findall(text)
    if not blocks:
        # unterminated block (e.g. truncated output) or raw code
        m = re.search(r"```(?:python|py)?[ \t]*\n(.*)", text, re.DOTALL)
        return (m.group(1) if m else text).strip()
    for b in reversed(blocks):
        if re.search(rf"def\s+{re.escape(entry_point)}\b", b):
            return b.strip()
    return blocks[-1].strip()
