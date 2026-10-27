from .base import Problem


def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    pre = 1
    for i in range(n):
        out[i] = pre
        pre *= nums[i]
    suf = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suf
        suf *= nums[i]
    return out


def _gen(rng):
    return [
        [[rng.choice([1, -1, 2, 3]) for _ in range(2000)]],
        [[rng.choice([0, 1, -1]) for _ in range(5000)]],
        [[rng.choice([1, -1]) for _ in range(100000)]],
    ]


PROBLEM = Problem(
    id="product_except_self",
    title="Product of Array Except Self",
    difficulty="medium",
    entry_point="product_except_self",
    prompt=(
        "Given a list `nums` with at least two integers, return a list `out` where `out[i]` is the "
        "product of all elements of `nums` except `nums[i]`. Do not use division (the input may "
        "contain zeros). Aim for O(n) time."
    ),
    starter="def product_except_self(nums: list[int]) -> list[int]:\n    ...",
    reference=product_except_self,
    cases=[
        ([[1, 2, 3, 4]], [24, 12, 8, 6]),
        ([[-1, 1, 0, -3, 3]], [0, 0, 9, 0, 0]),
        ([[2, 3]], [3, 2]),
        ([[0, 0]], [0, 0]),
        ([[0, 4, 5]], [20, 0, 0]),
    ],
    gen_args=_gen,
    tags=["array", "prefix-sum"],
)
