from .base import Problem


def is_match(s, p):
    n, m = len(s), len(p)
    prev = [False] * (m + 1)
    prev[0] = True
    for j in range(2, m + 1):
        prev[j] = p[j - 1] == "*" and prev[j - 2]
    for i in range(1, n + 1):
        cur = [False] * (m + 1)
        for j in range(1, m + 1):
            if p[j - 1] == "*":
                cur[j] = cur[j - 2] or (p[j - 2] in (".", s[i - 1]) and prev[j])
            else:
                cur[j] = p[j - 1] in (".", s[i - 1]) and prev[j - 1]
        prev = cur
    return prev[m]


def _gen(rng):
    # Patterns like "a*a*a*...b" against "aaa...a" blow up plain backtracking.
    cases = [["a" * 1000, "a*" * 500 + "b"], ["a" * 1000, "a*" * 500 + "a"], ["a" * 800, ".*" * 300 + "b"]]
    for _ in range(2):
        s = "".join(rng.choice("ab") for _ in range(600))
        parts = []
        for _ in range(250):
            parts.append(rng.choice("ab.") + rng.choice(["", "*", "*"]))
        cases.append([s, "".join(parts)])
    return cases


PROBLEM = Problem(
    id="regex_matching",
    title="Regular Expression Matching",
    difficulty="hard",
    entry_point="is_match",
    prompt=(
        "Implement matching of the string `s` against the pattern `p`, where `.` matches any single "
        "character and `x*` matches zero or more occurrences of the preceding element `x` (a letter or `.`). "
        "The match must cover the entire string, not just a part of it. `s` contains lowercase letters only "
        "and may be empty. `p` contains lowercase letters, `.` and `*`; every `*` follows a letter or `.`, "
        "and `p` may be empty. Both can be up to ~1000 characters, so exponential backtracking is too slow."
    ),
    starter="def is_match(s: str, p: str) -> bool:\n    ...",
    reference=is_match,
    cases=[
        (["aa", "a"], False), (["aa", "a*"], True), (["ab", ".*"], True), (["aab", "c*a*b"], True),
        (["mississippi", "mis*is*p*."], False), (["", ""], True), (["", "a*"], True), (["", ".*"], True),
        (["a", ""], False), (["abc", "abc"], True), (["abc", "ab"], False), (["ab", ".*c"], False),
        (["aaa", "a*a"], True), (["aaa", "ab*a*c*a"], True), (["a", "ab*"], True), (["bbbba", ".*a*a"], True),
    ],
    gen_args=_gen,
    tags=["dp", "string"],
)
