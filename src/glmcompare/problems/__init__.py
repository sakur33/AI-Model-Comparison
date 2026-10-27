"""Problem registry. Every non-underscore module exposes a `PROBLEM`."""
from __future__ import annotations

import importlib
import pkgutil
from functools import lru_cache

from .base import Problem

_ORDER = {"easy": 0, "medium": 1, "hard": 2}


@lru_cache(maxsize=1)
def load_all() -> dict[str, Problem]:
    problems: list[Problem] = []
    for mod in pkgutil.iter_modules(__path__):
        if mod.name == "base" or mod.name.startswith("_"):
            continue
        m = importlib.import_module(f"{__name__}.{mod.name}")
        problems.append(m.PROBLEM)
    problems.sort(key=lambda p: (_ORDER[p.difficulty], p.id))
    return {p.id: p for p in problems}


def get(problem_id: str) -> Problem:
    return load_all()[problem_id]
