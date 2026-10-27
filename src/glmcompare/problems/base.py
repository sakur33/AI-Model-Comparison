"""Problem definition shared by all problem modules."""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from typing import Any, Callable

Checker = Callable[[list, Any, Any], bool]  # (args, got, expected) -> ok


def jsonify(x: Any) -> Any:
    """Normalise tuples/etc. exactly as they will look after a JSON round-trip."""
    return json.loads(json.dumps(x))


def with_norm(fn: Callable[[Any], Any]) -> Checker:
    """Checker comparing fn(got) == fn(expected)."""
    return lambda args, got, expected: fn(got) == fn(expected)


def approx(tol: float = 1e-6) -> Checker:
    return lambda args, got, expected: (
        isinstance(got, (int, float)) and abs(got - expected) <= tol
    )


@dataclass
class Problem:
    id: str
    title: str
    difficulty: str  # easy | medium | hard
    entry_point: str
    prompt: str  # statement shown to the model
    starter: str  # signature shown to the model
    reference: Callable  # self-contained (imports inside); name == entry_point
    cases: list[tuple[list, Any]]  # hand-written (args, expected)
    gen_args: Callable[[random.Random], list[list]] | None = None  # bigger cases
    checker: Checker | None = None  # default: got == expected
    tags: list[str] = field(default_factory=list)

    def all_cases(self) -> list[tuple[list, Any]]:
        """Hand-written cases + generated ones (expected from the reference)."""
        out = [(list(a), e) for a, e in self.cases]
        if self.gen_args:
            rng = random.Random(f"{self.id}-v1")  # deterministic
            for args in self.gen_args(rng):
                out.append((args, self.reference(*json.loads(json.dumps(args)))))
        return out

    def check(self, args: list, got: Any, expected: Any) -> bool:
        expected = jsonify(expected)
        if self.checker is None:
            return got == expected
        return bool(self.checker(args, got, expected))
