from .base import Problem


def merge_intervals(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def _gen(rng):
    def mk(n, span):
        res = []
        for _ in range(n):
            s = rng.randint(0, span)
            res.append([s, s + rng.randint(0, 20)])
        return res
    return [[mk(50000, 10**6)], [mk(50000, 100000)], [mk(100, 500)]]


PROBLEM = Problem(
    id="merge_intervals",
    title="Merge Intervals",
    difficulty="medium",
    entry_point="merge_intervals",
    prompt=(
        "Given a list of closed intervals `[start, end]` (unsorted, `start <= end`), merge all "
        "overlapping intervals and return the result sorted by start. Intervals that touch "
        "(e.g. `[1,4]` and `[4,5]`) are considered overlapping."
    ),
    starter="def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n    ...",
    reference=merge_intervals,
    cases=[
        ([[[1, 3], [2, 6], [8, 10], [15, 18]]], [[1, 6], [8, 10], [15, 18]]),
        ([[[1, 4], [4, 5]]], [[1, 5]]),
        ([[[1, 4], [0, 4]]], [[0, 4]]),
        ([[[1, 4], [2, 3]]], [[1, 4]]),
        ([[]], []),
        ([[[5, 6], [1, 2], [3, 4]]], [[1, 2], [3, 4], [5, 6]]),
        ([[[1, 10], [2, 3], [4, 5], [6, 7]]], [[1, 10]]),
    ],
    gen_args=_gen,
    tags=["array", "sorting"],
)
