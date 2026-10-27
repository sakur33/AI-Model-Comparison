from .base import Problem


def min_window(s, t):
    from collections import Counter

    if not t or len(t) > len(s):
        return ""
    need = Counter(t)
    missing = len(t)
    best_len, best_start = len(s) + 1, 0
    left = 0
    for right, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_len, best_start = right - left + 1, left
            need[s[left]] += 1
            missing += 1
            left += 1
    return "" if best_len > len(s) else s[best_start:best_start + best_len]


def _gen(rng):
    mk = lambda n, a: "".join(rng.choice(a) for _ in range(n))
    return [
        [mk(100000, "abcde"), "abcdeeea"],
        [mk(50000, "abcdefghij"), "jjjjjiiiii"],
        [mk(200, "ab"), "aabbaabb"],
        [mk(1000, "abc"), "zz"],
    ]


PROBLEM = Problem(
    id="min_window_substring",
    title="Minimum Window Substring",
    difficulty="hard",
    entry_point="min_window",
    prompt=(
        "Return the shortest substring of `s` that contains every character of `t`, including "
        "duplicates (if `t` has two 'a', the window needs at least two 'a'). If no window exists, "
        "or `t` is empty, return an empty string. If several shortest windows exist, return the "
        "leftmost one. `s` can be up to 100,000 characters."
    ),
    starter="def min_window(s: str, t: str) -> str:\n    ...",
    reference=min_window,
    cases=[
        (["ADOBECODEBANC", "ABC"], "BANC"), (["a", "a"], "a"), (["a", "aa"], ""), (["ab", "b"], "b"),
        (["aa", "aa"], "aa"), (["abc", ""], ""), (["cabwefgewcwaefgcf", "cae"], "cwae"),
        (["abcabc", "cba"], "abc"),
    ],
    gen_args=_gen,
    tags=["sliding-window", "string", "hash-map"],
)
