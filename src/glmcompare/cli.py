"""Command line interface: list | validate | run | report."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from . import problems as problems_pkg
from .config import DEFAULT_RESULTS, Pricing, load_models
from .report import load_records, write_outputs
from .runner import run
from .sandbox import evaluate


def _select(ids: list[str] | None, difficulty: list[str] | None):
    allp = problems_pkg.load_all()
    if ids:
        missing = [i for i in ids if i not in allp]
        if missing:
            sys.exit(f"Unknown problem ids: {missing}. Use `glmcompare list`.")
        sel = [allp[i] for i in ids]
    else:
        sel = list(allp.values())
    if difficulty:
        sel = [p for p in sel if p.difficulty in difficulty]
    return sel


def _run_dir(results_dir: Path, run_id: str) -> Path:
    if run_id == "latest":
        runs = sorted(d for d in results_dir.glob("*") if d.is_dir())
        if not runs:
            sys.exit(f"No runs found in {results_dir}")
        return runs[-1]
    return results_dir / run_id


def cmd_list(args):
    for p in problems_pkg.load_all().values():
        print(f"{p.difficulty:7s} {p.id:34s} {len(p.all_cases()):3d} cases  {p.title}")


def cmd_validate(args):
    """Run every reference solution through the harness. Must be 100% green."""
    bad = 0
    for p in _select(args.problems, args.difficulty):
        ev = evaluate(p, _source(p), per_case_timeout=args.timeout)
        print(f"{'OK  ' if ev.passed else 'FAIL'} {p.id:34s} {ev.n_passed}/{ev.n_cases}")
        if not ev.passed:
            bad += 1
            print("     ", ev.error or ev.failures)
    sys.exit(1 if bad else 0)


def _source(p) -> str:
    import inspect
    return inspect.getsource(p.reference)


def cmd_run(args):
    models = load_models(args.config)
    unknown = [m for m in args.models if m not in models]
    if unknown:
        sys.exit(f"Unknown models {unknown}. Defined: {list(models)}")
    run_id = args.run_id or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = Path(args.results_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    sel = _select(args.problems, args.difficulty)
    print(f"Run '{run_id}': {len(args.models)} models x {len(sel)} problems x {args.samples} samples")
    run([models[m] for m in args.models], sel, args.samples, run_dir,
        workers=args.workers, per_case_timeout=args.timeout)
    print()
    print(write_outputs(run_dir, load_records(run_dir), models, run_id))
    print(f"Saved to {run_dir}")


def cmd_report(args):
    models = load_models(args.config)
    for spec in args.price or []:  # KEY=IN,OUT[,CACHE]
        key, vals = spec.split("=")
        nums = [float(v) for v in vals.split(",")]
        models[key].pricing = Pricing(*nums)
    run_dir = _run_dir(Path(args.results_dir), args.run_id)
    print(write_outputs(run_dir, load_records(run_dir), models, run_dir.name))


def main(argv=None):
    load_dotenv()
    ap = argparse.ArgumentParser(prog="glmcompare")
    ap.add_argument("--config", default=None, help="path to models.yaml")
    ap.add_argument("--results-dir", default=str(DEFAULT_RESULTS))
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_select(p):
        p.add_argument("--problems", nargs="+", help="problem ids (default: all)")
        p.add_argument("--difficulty", nargs="+", choices=["easy", "medium", "hard"])

    sub.add_parser("list", help="list problems").set_defaults(fn=cmd_list)

    p = sub.add_parser("validate", help="check the harness against reference solutions")
    add_select(p)
    p.add_argument("--timeout", type=float, default=10.0)
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("run", help="query models and evaluate their solutions")
    add_select(p)
    p.add_argument("--models", nargs="+", required=True)
    p.add_argument("--samples", type=int, default=1, help="attempts per problem")
    p.add_argument("--run-id", default=None, help="reuse an id to resume a run")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--timeout", type=float, default=5.0, help="seconds per test case")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("report", help="(re)build the report for a run")
    p.add_argument("--run-id", default="latest")
    p.add_argument("--price", action="append", metavar="KEY=IN,OUT[,CACHE]",
                   help="override USD/1M-token prices, e.g. glm=0.6,2.2")
    p.set_defaults(fn=cmd_report)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
