import inspect

import pytest

from glmcompare import problems
from glmcompare.config import Pricing, load_models
from glmcompare.pricing import cost_usd
from glmcompare.prompts import extract_code
from glmcompare.report import load_records, summarise, write_outputs
from glmcompare.runner import run
from glmcompare.sandbox import evaluate

ALL = list(problems.load_all().values())


def test_problem_metadata():
    assert len(ALL) >= 20
    ids = [p.id for p in ALL]
    assert len(ids) == len(set(ids))
    for p in ALL:
        assert p.difficulty in {"easy", "medium", "hard"}
        assert p.reference.__name__ == p.entry_point
        assert f"def {p.entry_point}" in p.starter


@pytest.mark.parametrize("p", ALL, ids=lambda p: p.id)
def test_reference_passes(p):
    ev = evaluate(p, inspect.getsource(p.reference), per_case_timeout=10)
    assert ev.passed, (ev.error, ev.failures)


P = problems.get("two_sum")


def test_wrong_answer():
    ev = evaluate(P, "def two_sum(nums, target):\n    return [0, 0]")
    assert not ev.passed and ev.failures


def test_exception_and_syntax_error():
    assert not evaluate(P, "def two_sum(nums, target):\n    raise ValueError('x')").passed
    ev = evaluate(P, "def two_sum(:")
    assert not ev.passed and "SyntaxError" in ev.error


def test_missing_function():
    ev = evaluate(P, "x = 1")
    assert not ev.passed and "not defined" in ev.error


def test_timeout_is_enforced():
    code = "def two_sum(nums, target):\n    while True:\n        pass"
    ev = evaluate(P, code, per_case_timeout=0.5)
    assert not ev.passed and ev.failures[0]["reason"].startswith("timeout")


def test_swallowed_exception_cannot_defeat_timeout():
    code = (
        "def two_sum(nums, target):\n"
        "    while True:\n"
        "        try:\n            while True: pass\n        except Exception:\n            pass"
    )
    assert not evaluate(P, code, per_case_timeout=0.5).passed


def test_solution_class_style_accepted():
    code = (
        "class Solution:\n"
        "    def two_sum(self, nums, target):\n"
        "        seen = {}\n"
        "        for i, x in enumerate(nums):\n"
        "            if target - x in seen: return [seen[target - x], i]\n"
        "            seen[x] = i\n"
    )
    assert evaluate(P, code).passed


def test_prints_do_not_break_harness():
    code = (
        "def two_sum(nums, target):\n    print('hello')\n"
        "    d = {}\n"
        "    for i, x in enumerate(nums):\n"
        "        if target - x in d: return [d[target - x], i]\n"
        "        d[x] = i\n"
    )
    assert evaluate(P, code).passed


def test_inefficient_solution_fails_large_case():
    p = problems.get("sliding_window_maximum")
    code = (
        "def max_sliding_window(nums, k):\n"
        "    return [max(nums[i:i+k]) for i in range(len(nums)-k+1)]"
    )
    assert not evaluate(p, code, per_case_timeout=2).passed


def test_extract_code():
    text = "Here:\n```python\ndef helper(): pass\n```\nand\n```python\ndef f(x):\n    return x\n```"
    assert extract_code(text, "f").startswith("def f")
    assert extract_code("```python\ndef f(): pass", "f") == "def f(): pass"  # truncated
    assert extract_code("def f(): pass", "f") == "def f(): pass"


def test_pricing():
    pr = Pricing(input_per_mtok=3.0, output_per_mtok=15.0, cache_read_per_mtok=0.3)
    assert cost_usd(1_000_000, 100_000, pr) == pytest.approx(4.5)
    assert cost_usd(0, 0, pr, cache_read_tokens=1_000_000) == pytest.approx(0.3)
    assert cost_usd(10, 10, Pricing()) is None


def test_end_to_end_with_mock(tmp_path):
    models = load_models()
    sel = [problems.get(i) for i in ("two_sum", "n_queens", "coin_change")]
    run_dir = tmp_path / "r1"
    run([models["mock"]], sel, samples=2, run_dir=run_dir, workers=2, per_case_timeout=10, log=lambda *_: None)
    recs = load_records(run_dir)
    assert len(recs) == 6 and all(r["passed"] for r in recs)
    s = summarise(recs, models)["mock"]
    assert s["pass_rate"] == 1.0 and s["cost_per_task"] > 0
    md = write_outputs(run_dir, recs, models, "r1")
    assert "Cost / solved task" in md
    assert (run_dir / "per_task.csv").exists()
    # resume: nothing is re-queried
    run([models["mock"]], sel, samples=2, run_dir=run_dir, workers=2, log=lambda *_: None)
