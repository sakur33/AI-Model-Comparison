from .base import Problem


def min_distance(word1, word2):
    if len(word1) < len(word2):
        word1, word2 = word2, word1
    prev = list(range(len(word2) + 1))
    for i, a in enumerate(word1, 1):
        cur = [i]
        for j, b in enumerate(word2, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a != b)))
        prev = cur
    return prev[-1]


def _gen(rng):
    mk = lambda n: "".join(rng.choice("abcd") for _ in range(n))
    return [[mk(1000), mk(1000)], [mk(1500), mk(700)], [mk(500), mk(500)]]


PROBLEM = Problem(
    id="edit_distance",
    title="Edit Distance",
    difficulty="hard",
    entry_point="min_distance",
    prompt=(
        "Return the minimum number of single-character operations (insert, delete, replace) needed "
        "to turn `word1` into `word2`. Strings can be up to ~1500 characters, either may be empty."
    ),
    starter="def min_distance(word1: str, word2: str) -> int:\n    ...",
    reference=min_distance,
    cases=[
        (["horse", "ros"], 3), (["intention", "execution"], 5), (["", ""], 0), (["", "abc"], 3),
        (["abc", ""], 3), (["abc", "abc"], 0), (["kitten", "sitting"], 3), (["sunday", "saturday"], 3),
    ],
    gen_args=_gen,
    tags=["dp", "string"],
)
