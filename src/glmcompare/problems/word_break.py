from .base import Problem


def word_break(s, word_dict):
    words = set(word_dict)
    lengths = sorted({len(w) for w in words})
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for L in lengths:
            if L > i:
                break
            if dp[i - L] and s[i - L:i] in words:
                dp[i] = True
                break
    return dp[len(s)]


def _gen(rng):
    return [
        ["a" * 3000 + "b", ["a", "aa", "aaa", "aaaa"]],
        ["a" * 3000, ["aaaa", "aaaaaaa"]],
        ["ab" * 1500, ["a", "b", "ab", "ba"]],
        ["".join(rng.choice("ab") for _ in range(2000)), ["a", "ab", "bab", "bba", "abb"]],
    ]


PROBLEM = Problem(
    id="word_break",
    title="Word Break",
    difficulty="medium",
    entry_point="word_break",
    prompt=(
        "Return `True` if the string `s` can be split into a sequence of one or more words from "
        "`word_dict` (words may be reused). The empty string counts as segmentable. Strings can be "
        "a few thousand characters long, so naive backtracking will time out."
    ),
    starter="def word_break(s: str, word_dict: list[str]) -> bool:\n    ...",
    reference=word_break,
    cases=[
        (["leetcode", ["leet", "code"]], True),
        (["applepenapple", ["apple", "pen"]], True),
        (["catsandog", ["cats", "dog", "sand", "and", "cat"]], False),
        (["", ["a"]], True),
        (["a", []], False),
        (["aaaaaaa", ["aaaa", "aaa"]], True),
    ],
    gen_args=_gen,
    tags=["dp", "string"],
)
