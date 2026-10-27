from .base import Problem


def max_profit(prices):
    best, low = 0, float("inf")
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best


def _gen(rng):
    return [
        [[rng.randint(0, 10**4) for _ in range(300000)]],
        [list(range(200000, 0, -1))],
        [[rng.randint(0, 100) for _ in range(1000)]],
    ]


PROBLEM = Problem(
    id="best_time_to_buy_sell_stock",
    title="Best Time to Buy and Sell Stock",
    difficulty="easy",
    entry_point="max_profit",
    prompt=(
        "`prices[i]` is the price of a stock on day `i`. You may buy once and sell once on a later day. "
        "Return the maximum profit you can make, or 0 if no profit is possible."
    ),
    starter="def max_profit(prices: list[int]) -> int:\n    ...",
    reference=max_profit,
    cases=[
        ([[7, 1, 5, 3, 6, 4]], 5), ([[7, 6, 4, 3, 1]], 0), ([[1]], 0), ([[]], 0),
        ([[2, 4, 1]], 2), ([[3, 2, 6, 5, 0, 3]], 4), ([[5, 5, 5]], 0),
    ],
    gen_args=_gen,
    tags=["array", "greedy"],
)
