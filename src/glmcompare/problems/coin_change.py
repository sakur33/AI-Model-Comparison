from .base import Problem


def coin_change(coins, amount):
    INF = amount + 1
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1


def _gen(rng):
    return [
        [[186, 419, 83, 408], 6249],
        [[rng.randint(2, 500) for _ in range(12)], 10000],
        [[7, 13, 29, 101], 9999],
        [[2, 4, 6, 8], 9999],
    ]


PROBLEM = Problem(
    id="coin_change",
    title="Coin Change",
    difficulty="medium",
    entry_point="coin_change",
    prompt=(
        "Given distinct positive coin denominations `coins` (unlimited supply of each) and a "
        "non-negative integer `amount`, return the fewest coins needed to make exactly `amount`, "
        "or -1 if impossible. `amount` can be up to about 10^4."
    ),
    starter="def coin_change(coins: list[int], amount: int) -> int:\n    ...",
    reference=coin_change,
    cases=[
        ([[1, 2, 5], 11], 3), ([[2], 3], -1), ([[1], 0], 0), ([[186, 419, 83, 408], 6249], 20),
        ([[2, 5, 10, 1], 27], 4), ([[5, 7], 3], -1), ([[3, 7, 405, 436], 8839], 25),
    ],
    gen_args=_gen,
    tags=["dp"],
)
