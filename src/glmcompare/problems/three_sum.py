from .base import Problem, with_norm


def three_sum(nums):
    nums = sorted(nums)
    n, res = len(nums), []
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1
    return res


def _gen(rng):
    return [
        [[rng.randint(-500, 500) for _ in range(2000)]],
        [[rng.randint(-10**5, 10**5) for _ in range(2000)]],
        [[0] * 3000],
    ]


PROBLEM = Problem(
    id="three_sum",
    title="3Sum",
    difficulty="medium",
    entry_point="three_sum",
    prompt=(
        "Return all unique triplets `[a, b, c]` of values from `nums` (using three different indices) "
        "such that `a + b + c == 0`. The result must not contain duplicate triplets (triplets with the "
        "same multiset of values count as duplicates). Order of triplets and of values inside a triplet "
        "does not matter. Inputs can have a few thousand elements."
    ),
    starter="def three_sum(nums: list[int]) -> list[list[int]]:\n    ...",
    reference=three_sum,
    cases=[
        ([[-1, 0, 1, 2, -1, -4]], [[-1, -1, 2], [-1, 0, 1]]),
        ([[0, 1, 1]], []),
        ([[0, 0, 0]], [[0, 0, 0]]),
        ([[0, 0, 0, 0]], [[0, 0, 0]]),
        ([[]], []),
        ([[-2, 0, 1, 1, 2]], [[-2, 0, 2], [-2, 1, 1]]),
    ],
    gen_args=_gen,
    checker=with_norm(lambda g: sorted(sorted(t) for t in g)),
    tags=["array", "two-pointers", "sorting"],
)
