from .base import Problem


def trap(height):
    lo, hi = 0, len(height) - 1
    lmax = rmax = water = 0
    while lo < hi:
        if height[lo] < height[hi]:
            lmax = max(lmax, height[lo])
            water += lmax - height[lo]
            lo += 1
        else:
            rmax = max(rmax, height[hi])
            water += rmax - height[hi]
            hi -= 1
    return water


def _gen(rng):
    return [
        [[rng.randint(0, 10**4) for _ in range(300000)]],
        [[rng.randint(0, 5) for _ in range(1000)]],
        [[10**5 - i for i in range(100000)] + [i for i in range(100000)]],
    ]


PROBLEM = Problem(
    id="trapping_rain_water",
    title="Trapping Rain Water",
    difficulty="hard",
    entry_point="trap",
    prompt=(
        "`height[i]` is the height of a unit-width bar. After raining, return the total units of "
        "water trapped between the bars. The list can be empty and can have 300,000 elements; "
        "aim for O(n) time."
    ),
    starter="def trap(height: list[int]) -> int:\n    ...",
    reference=trap,
    cases=[
        ([[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], 6), ([[4, 2, 0, 3, 2, 5]], 9),
        ([[]], 0), ([[3]], 0), ([[3, 0, 3]], 3), ([[1, 2, 3]], 0), ([[5, 4, 1, 2]], 1),
    ],
    gen_args=_gen,
    tags=["two-pointers", "array"],
)
