"""Generate solutions with each model, evaluate them, persist results as JSON."""
from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .clients import make_client
from .config import ModelConfig
from .problems.base import Problem
from .prompts import SYSTEM_PROMPT, build_user_prompt, extract_code
from .sandbox import evaluate


def result_path(run_dir: Path, model_key: str, problem_id: str, sample: int) -> Path:
    return run_dir / model_key / problem_id / f"sample_{sample}.json"


def _call_with_retry(client, system, user, problem, retries=3):
    last = None
    for attempt in range(retries):
        try:
            return client.complete(system, user, problem=problem)
        except Exception as e:  # network, rate limit, 5xx ...
            last = e
            time.sleep(2 ** attempt * 2)
    raise last


def run_one(client, cfg: ModelConfig, problem: Problem, sample: int, run_dir: Path,
            per_case_timeout: float) -> dict:
    path = result_path(run_dir, cfg.key, problem.id, sample)
    if path.exists():
        prev = json.loads(path.read_text())
        if not prev.get("api_error"):
            return prev  # resumable: keep finished attempts
    rec = {
        "model_key": cfg.key,
        "model": cfg.model,
        "problem_id": problem.id,
        "difficulty": problem.difficulty,
        "sample": sample,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "api_error": None,
    }
    try:
        comp = _call_with_retry(client, SYSTEM_PROMPT, build_user_prompt(problem), problem)
    except Exception as e:
        rec.update(api_error=f"{type(e).__name__}: {e}"[:500], passed=False,
                   input_tokens=0, output_tokens=0, cache_read_tokens=0)
    else:
        code = extract_code(comp.text, problem.entry_point)
        ev = evaluate(problem, code, per_case_timeout)
        rec.update(
            response=comp.text,
            code=code,
            input_tokens=comp.input_tokens,
            output_tokens=comp.output_tokens,
            cache_read_tokens=comp.cache_read_tokens,
            latency_s=comp.latency_s,
            stop_reason=comp.stop_reason,
            passed=ev.passed,
            n_cases=ev.n_cases,
            n_passed=ev.n_passed,
            error=ev.error,
            failures=ev.failures,
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rec, indent=2))
    return rec


def run(models: list[ModelConfig], problems: list[Problem], samples: int, run_dir: Path,
        workers: int = 4, per_case_timeout: float = 5.0, log=print) -> list[dict]:
    clients = {m.key: make_client(m) for m in models}
    jobs = [(m, p, s) for m in models for p in problems for s in range(samples)]
    out = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {
            pool.submit(run_one, clients[m.key], m, p, s, run_dir, per_case_timeout): (m, p, s)
            for m, p, s in jobs
        }
        for i, fut in enumerate(as_completed(futs), 1):
            m, p, s = futs[fut]
            rec = fut.result()
            status = "API-ERROR" if rec.get("api_error") else ("PASS" if rec["passed"] else "FAIL")
            log(f"[{i}/{len(jobs)}] {m.key:10s} {p.id:32s} s{s} {status}")
            out.append(rec)
    return out
