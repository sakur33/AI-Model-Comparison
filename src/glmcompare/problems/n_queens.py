from .base import Problem


def total_n_queens(n):
    cols, d1, d2 = set(), set(), set()

    def go(r):
        if r == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or r - c in d1 or r + c in d2:
                continue
            cols.add(c); d1.add(r - c); d2.add(r + c)
            total += go(r + 1)
            cols.remove(c); d1.remove(r - c); d2.remove(r + c)
        return total

    return go(0)


PROBLEM = Problem(
    id="n_queens",
    title="N-Queens (count solutions)",
    difficulty="hard",
    entry_point="total_n_queens",
    prompt=(
        "Return the number of distinct ways to place `n` queens on an `n x n` chessboard so that no "
        "two queens attack each other (same row, column or diagonal). Tested for `1 <= n <= 10`; "
        "each call must finish within the time limit, so pruning is required."
    ),
    starter="def total_n_queens(n: int) -> int:\n    ...",
    reference=total_n_queens,
    cases=[([1], 1), ([2], 0), ([3], 0), ([4], 2), ([5], 10), ([6], 4), ([7], 40), ([8], 92),
           ([9], 352), ([10], 724)],
    tags=["backtracking"],
)
