from .base import Problem


def length_of_longest_substring(s):
    last, start, best = {}, 0, 0
    for i, c in enumerate(s):
        if c in last and last[c] >= start:
            start = last[c] + 1
        last[c] = i
        best = max(best, i - start + 1)
    return best


def _gen(rng):
    return [
        ["".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(200000))],
        ["".join(rng.choice("ab") for _ in range(200000))],
        [("abcdefghij" * 20000)],
    ]


PROBLEM = Problem(
    id="longest_substring_no_repeat",
    title="Longest Substring Without Repeating Characters",
    difficulty="medium",
    entry_point="length_of_longest_substring",
    prompt=(
        "Return the length of the longest contiguous substring of `s` that contains no repeated "
        "character. `s` may contain any ASCII characters, including spaces, and may be empty."
    ),
    starter="def length_of_longest_substring(s: str) -> int:\n    ...",
    reference=length_of_longest_substring,
    cases=[
        (["abcabcbb"], 3), (["bbbbb"], 1), (["pwwkew"], 3), ([""], 0), ([" "], 1),
        (["dvdf"], 3), (["abba"], 2), (["tmmzuxt"], 5),
    ],
    gen_args=_gen,
    tags=["sliding-window", "string"],
)
