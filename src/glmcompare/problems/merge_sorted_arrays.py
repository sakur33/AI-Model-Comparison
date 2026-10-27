from .base import Problem


def merge_sorted(a, b):
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def _gen(rng):
    mk = lambda n: sorted(rng.randint(-10**6, 10**6) for _ in range(n))
    return [[mk(200000), mk(150000)], [mk(10), mk(100000)], [mk(1000), []]]


PROBLEM = Problem(
    id="merge_sorted_arrays",
    title="Merge Two Sorted Lists",
    difficulty="easy",
    entry_point="merge_sorted",
    prompt=(
        "Given two lists of integers `a` and `b`, each sorted in non-decreasing order, return a new "
        "sorted list containing all elements of both. Do not modify the inputs. "
        "Aim for O(len(a) + len(b)) time."
    ),
    starter="def merge_sorted(a: list[int], b: list[int]) -> list[int]:\n    ...",
    reference=merge_sorted,
    cases=[
        ([[1, 2, 4], [1, 3, 4]], [1, 1, 2, 3, 4, 4]),
        ([[], []], []),
        ([[], [0]], [0]),
        ([[-5, -1], [-3]], [-5, -3, -1]),
        ([[1, 1, 1], [1, 1]], [1, 1, 1, 1, 1]),
    ],
    gen_args=_gen,
    tags=["array", "two-pointers"],
)
