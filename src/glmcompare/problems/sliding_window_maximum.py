from .base import Problem


def max_sliding_window(nums, k):
    from collections import deque

    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def _gen(rng):
    big = [rng.randint(-10**6, 10**6) for _ in range(200000)]
    return [
        [big, 1000],
        [big, 50000],
        [sorted(big), 5000],
        [sorted(big, reverse=True), 5000],
        [[rng.randint(0, 9) for _ in range(500)], 7],
    ]


PROBLEM = Problem(
    id="sliding_window_maximum",
    title="Sliding Window Maximum",
    difficulty="hard",
    entry_point="max_sliding_window",
    prompt=(
        "A window of size `k` slides from the left to the right of `nums`, one position at a time. "
        "Return the list of the maximum value in each window position (length `len(nums) - k + 1`). "
        "`1 <= k <= len(nums)`. `nums` can have 200,000 elements and `k` up to 50,000, so an O(n*k) "
        "solution will time out."
    ),
    starter="def max_sliding_window(nums: list[int], k: int) -> list[int]:\n    ...",
    reference=max_sliding_window,
    cases=[
        ([[1, 3, -1, -3, 5, 3, 6, 7], 3], [3, 3, 5, 5, 6, 7]), ([[1], 1], [1]), ([[1, -1], 1], [1, -1]),
        ([[9, 11], 2], [11]), ([[4, 3, 2, 1], 2], [4, 3, 2]), ([[1, 2, 3, 4], 4], [4]),
        ([[7, 2, 4], 2], [7, 4]),
    ],
    gen_args=_gen,
    tags=["deque", "sliding-window"],
)
