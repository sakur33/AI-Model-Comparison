"""Aggregate results into pass rate + cost-per-task tables."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from .config import ModelConfig
from .pricing import cost_usd


def load_records(run_dir: Path) -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(run_dir.glob("*/*/sample_*.json"))]


def _usd(x, digits=4):
    return "n/a" if x is None else f"${x:,.{digits}f}"


def summarise(records: list[dict], models: dict[str, ModelConfig]) -> dict[str, dict]:
    """Per-model metrics. Cost uses the *current* pricing in `models`."""
    by_model = defaultdict(list)
    for r in records:
        by_model[r["model_key"]].append(r)

    out = {}
    for key, rs in by_model.items():
        cfg = models.get(key)
        costs = [
            cost_usd(r["input_tokens"], r["output_tokens"], cfg.pricing, r.get("cache_read_tokens", 0))
            if cfg else None
            for r in rs
        ]
        known = None if any(c is None for c in costs) else sum(costs)
        solved = sum(1 for r in rs if r["passed"])
        by_diff = defaultdict(lambda: [0, 0])
        for r in rs:
            by_diff[r["difficulty"]][1] += 1
            by_diff[r["difficulty"]][0] += int(r["passed"])
        lat = [r["latency_s"] for r in rs if r.get("latency_s")]
        out[key] = {
            "label": cfg.label if cfg else key,
            "attempts": len(rs),
            "solved": solved,
            "pass_rate": solved / len(rs),
            "by_difficulty": {d: tuple(v) for d, v in by_diff.items()},
            "input_tokens": sum(r["input_tokens"] for r in rs),
            "output_tokens": sum(r["output_tokens"] for r in rs),
            "avg_output_tokens": sum(r["output_tokens"] for r in rs) / len(rs),
            "total_cost": known,
            "cost_per_task": None if known is None else known / len(rs),
            "cost_per_solved": None if known is None or solved == 0 else known / solved,
            "avg_latency_s": sum(lat) / len(lat) if lat else None,
            "api_errors": sum(1 for r in rs if r.get("api_error")),
        }
    return out


def to_markdown(summary: dict[str, dict], run_id: str) -> str:
    keys = list(summary)
    lines = [f"# Results: {run_id}", ""]
    lines += [
        "| Model | Attempts | Solved | Pass rate | Avg out tok | Total cost | Cost / task | Cost / solved task | Avg latency |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for k in keys:
        s = summary[k]
        lat = "n/a" if s["avg_latency_s"] is None else f"{s['avg_latency_s']:.1f}s"
        lines.append(
            f"| {s['label']} | {s['attempts']} | {s['solved']} | {s['pass_rate']:.1%} | "
            f"{s['avg_output_tokens']:.0f} | {_usd(s['total_cost'], 2)} | {_usd(s['cost_per_task'], 5)} | "
            f"{_usd(s['cost_per_solved'], 5)} | {lat} |"
        )
    diffs = ["easy", "medium", "hard"]
    lines += ["", "## Pass rate by difficulty", "", "| Model | " + " | ".join(diffs) + " |",
              "|---|" + "---|" * len(diffs)]
    for k in keys:
        cells = []
        for d in diffs:
            ok, n = summary[k]["by_difficulty"].get(d, (0, 0))
            cells.append(f"{ok}/{n}" if n else "-")
        lines.append(f"| {summary[k]['label']} | " + " | ".join(cells) + " |")
    if len(keys) >= 2:
        a, b = summary[keys[0]], summary[keys[1]]
        lines += ["", "## Cost comparison", ""]
        for metric, name in (("cost_per_task", "cost per task"), ("cost_per_solved", "cost per solved task")):
            if a[metric] and b[metric]:
                lines.append(
                    f"- {name}: {a['label']} is {a[metric] / b[metric]:.2f}x {b['label']} "
                    f"({_usd(a[metric], 5)} vs {_usd(b[metric], 5)})"
                )
    errs = [summary[k]["label"] for k in keys if summary[k]["api_errors"]]
    if errs:
        lines += ["", f"WARNING: API errors present for: {', '.join(errs)} (re-run to retry them)."]
    if any(summary[k]["total_cost"] is None for k in keys):
        lines += ["", "NOTE: some prices are not set in config/models.yaml, costs show n/a."]
    return "\n".join(lines) + "\n"


def write_outputs(run_dir: Path, records: list[dict], models: dict[str, ModelConfig], run_id: str) -> str:
    summary = summarise(records, models)
    md = to_markdown(summary, run_id)
    (run_dir / "report.md").write_text(md)
    with open(run_dir / "per_task.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "problem", "difficulty", "sample", "passed", "n_passed", "n_cases",
                    "input_tokens", "output_tokens", "cache_read_tokens", "latency_s", "cost_usd", "error"])
        for r in records:
            cfg = models.get(r["model_key"])
            c = cost_usd(r["input_tokens"], r["output_tokens"], cfg.pricing,
                         r.get("cache_read_tokens", 0)) if cfg else None
            w.writerow([r["model_key"], r["problem_id"], r["difficulty"], r["sample"], r["passed"],
                        r.get("n_passed"), r.get("n_cases"), r["input_tokens"], r["output_tokens"],
                        r.get("cache_read_tokens", 0), r.get("latency_s"), c,
                        r.get("api_error") or r.get("error") or ""])
    return md
