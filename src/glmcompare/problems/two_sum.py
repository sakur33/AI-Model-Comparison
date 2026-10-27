from .base import Problem


def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []


def _gen(rng):
    cases = []
    for n in (5000, 50000):
        nums = [rng.randint(-10**9, 10**9) for _ in range(n)]
        i, j = rng.sample(range(n), 2)
        cases.append([nums, nums[i] + nums[j]])
    return cases


def _check(args, got, expected):
    nums, target = args
    return (
        isinstance(got, list)
        and len(got) == 2
        and got[0] != got[1]
        and all(isinstance(k, int) and 0 <= k < len(nums) for k in got)
        and nums[got[0]] + nums[got[1]] == target
    )


PROBLEM = Problem(
    id="two_sum",
    title="Two Sum",
    difficulty="easy",
    entry_point="two_sum",
    prompt=(
        "Given a list of integers `nums` and an integer `target`, return a list `[i, j]` of two "
        "different indices such that `nums[i] + nums[j] == target`. Exactly one valid pair of values "
        "exists; any valid index pair is accepted, in any order. You may not use the same element twice."
    ),
    starter="def two_sum(nums: list[int], target: int) -> list[int]:\n    ...",
    reference=two_sum,
    cases=[
        ([[2, 7, 11, 15], 9], [0, 1]),
        ([[3, 2, 4], 6], [1, 2]),
        ([[3, 3], 6], [0, 1]),
        ([[-1, -2, -3, -4, -5], -8], [2, 4]),
        ([[0, 4, 3, 0], 0], [0, 3]),
    ],
    gen_args=_gen,
    checker=_check,
    tags=["array", "hash-map"],
)
