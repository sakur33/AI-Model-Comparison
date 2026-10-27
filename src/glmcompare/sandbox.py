"""Host side of the test harness: run candidate code against a problem's cases.

Isolation is process-level only (separate interpreter, temp cwd, timeouts). It is
NOT a security sandbox: only run code from models you are evaluating, ideally
inside a container/VM if you are worried about it.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .problems.base import Problem

CHILD = Path(__file__).with_name("_child.py")


@dataclass
class EvalResult:
    passed: bool
    n_cases: int
    n_passed: int
    error: str | None = None  # setup / crash / wall-clock timeout
    failures: list[dict] = field(default_factory=list)  # first few failing cases


def _short(x, n=200) -> str:
    s = repr(x)
    return s if len(s) <= n else s[:n] + "..."


def evaluate(problem: Problem, code: str, per_case_timeout: float = 5.0) -> EvalResult:
    cases = problem.all_cases()
    payload = {
        "code": code,
        "entry_point": problem.entry_point,
        "cases": [a for a, _ in cases],
        "per_case_timeout": per_case_timeout,
    }
    with tempfile.TemporaryDirectory(prefix="glmcompare_") as tmp:
        pj, rj = Path(tmp) / "payload.json", Path(tmp) / "result.json"
        pj.write_text(json.dumps(payload))
        try:
            subprocess.run(
                [sys.executable, "-I", str(CHILD), str(pj), str(rj)],
                cwd=tmp,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                timeout=per_case_timeout * len(cases) + 15,
            )
        except subprocess.TimeoutExpired:
            return EvalResult(False, len(cases), 0, error="wall-clock timeout")
        if not rj.exists():
            return EvalResult(False, len(cases), 0, error="child crashed (no result)")
        res = json.loads(rj.read_text())

    if res["setup_error"]:
        return EvalResult(False, len(cases), 0, error=res["setup_error"])

    n_passed, failures = 0, []
    for i, ((args, expected), r) in enumerate(zip(cases, res["results"])):
        ok, why = False, None
        if r["ok"]:
            try:
                ok = problem.check(args, r["out"], expected)
            except Exception as e:  # malformed output shape etc.
                why = f"checker error: {type(e).__name__}"
            if not ok and why is None:
                why = f"wrong answer: got {_short(r['out'])} expected {_short(expected)}"
        else:
            why = r["error"]
        if ok:
            n_passed += 1
        elif len(failures) < 3:
            failures.append({"case": i, "input": _short(args, 150), "reason": why})
    return EvalResult(n_passed == len(cases), len(cases), n_passed, failures=failures)
