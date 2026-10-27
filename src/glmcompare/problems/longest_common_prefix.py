from .base import Problem


def longest_common_prefix(strs):
    if not strs:
        return ""
    first = min(strs)
    last = max(strs)
    i = 0
    while i < len(first) and i < len(last) and first[i] == last[i]:
        i += 1
    return first[:i]


def _gen(rng):
    pre = "".join(rng.choice("ab") for _ in range(5000))
    words = [pre + "".join(rng.choice("abc") for _ in range(rng.randint(0, 30))) for _ in range(500)]
    return [[words], [[pre] * 1000]]


PROBLEM = Problem(
    id="longest_common_prefix",
    title="Longest Common Prefix",
    difficulty="easy",
    entry_point="longest_common_prefix",
    prompt=(
        "Return the longest string that is a prefix of every string in `strs`. "
        "Return an empty string if there is none (or if `strs` is empty)."
    ),
    starter="def longest_common_prefix(strs: list[str]) -> str:\n    ...",
    reference=longest_common_prefix,
    cases=[
        ([["flower", "flow", "flight"]], "fl"),
        ([["dog", "racecar", "car"]], ""),
        ([["a"]], "a"),
        ([["", ""]], ""),
        ([["ab", "a"]], "a"),
        ([["interview", "internet", "interval", "internal"]], "inter"),
        ([[]], ""),
    ],
    gen_args=_gen,
    tags=["string"],
)
