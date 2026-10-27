"""Runs untrusted model code in a separate process.

Usage: python -I _child.py payload.json result.json
Executed standalone (not imported) so it shares nothing with the host.
"""
import copy
import json
import os
import signal
import sys
import traceback


class _Timeout(BaseException):  # BaseException so user `except Exception` can't swallow it
    pass


def _on_alarm(signum, frame):
    raise _Timeout()


def main(payload_path, result_path):
    sys.set_int_max_str_digits(0)
    sys.setrecursionlimit(10000)
    with open(payload_path) as f:
        payload = json.load(f)

    results = []
    real_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    ns = {"__name__": "candidate"}

    def finish(extra=None):
        sys.stdout = real_stdout
        out = {"setup_error": None, "results": results}
        if extra:
            out.update(extra)
        with open(result_path, "w") as f:
            json.dump(out, f)

    try:
        exec(compile(payload["code"], "<candidate>", "exec"), ns)
        name = payload["entry_point"]
        if name in ns and callable(ns[name]):
            fn = ns[name]
        elif "Solution" in ns:
            fn = getattr(ns["Solution"](), name)
        else:
            raise NameError(f"function '{name}' not defined")
    except BaseException:
        finish({"setup_error": traceback.format_exc(limit=3)[-1500:]})
        return

    signal.signal(signal.SIGALRM, _on_alarm)
    timed_out = False
    for args in payload["cases"]:
        if timed_out:
            results.append({"ok": False, "error": "skipped after earlier timeout"})
            continue
        args = copy.deepcopy(args)
        try:
            signal.setitimer(signal.ITIMER_REAL, payload["per_case_timeout"])
            out = fn(*args)
            signal.setitimer(signal.ITIMER_REAL, 0)
            json.dumps(out)  # must be serialisable
            results.append({"ok": True, "out": out})
        except _Timeout:
            timed_out = True
            results.append({"ok": False, "error": f"timeout > {payload['per_case_timeout']}s"})
        except RecursionError:
            signal.setitimer(signal.ITIMER_REAL, 0)
            results.append({"ok": False, "error": "RecursionError"})
        except BaseException as e:
            signal.setitimer(signal.ITIMER_REAL, 0)
            results.append({"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"})
    finish()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
