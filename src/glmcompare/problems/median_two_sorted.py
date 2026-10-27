from .base import Problem, approx


def find_median(a, b):
    m = sorted(a + b)  # reference favours clarity; candidates may be O(log n)
    n = len(m)
    return float(m[n // 2]) if n % 2 else (m[n // 2 - 1] + m[n // 2]) / 2


def _gen(rng):
    mk = lambda n: sorted(rng.randint(-10**6, 10**6) for _ in range(n))
    return [[mk(100000), mk(100000)], [mk(1), mk(99999)], [mk(3000), mk(7)]]


PROBLEM = Problem(
    id="median_two_sorted",
    title="Median of Two Sorted Arrays",
    difficulty="hard",
    entry_point="find_median",
    prompt=(
        "Given two sorted lists of integers `a` and `b` (not both empty), return the median of the "
        "combined values as a float. For an even total count, the median is the mean of the two "
        "middle values. The ideal solution runs in O(log(len(a) + len(b))), but any correct and "
        "reasonably fast solution is accepted."
    ),
    starter="def find_median(a: list[int], b: list[int]) -> float:\n    ...",
    reference=find_median,
    cases=[
        ([[1, 3], [2]], 2.0), ([[1, 2], [3, 4]], 2.5), ([[], [1]], 1.0), ([[0, 0], [0, 0]], 0.0),
        ([[], [2, 3]], 2.5), ([[1], [2, 3, 4, 5, 6]], 3.5), ([[-5, 3, 6, 12, 15], [-12, -10, -6, -3, 4, 10]], 3.0),
    ],
    gen_args=_gen,
    checker=approx(1e-6),
    tags=["binary-search", "array"],
)
