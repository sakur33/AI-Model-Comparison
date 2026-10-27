from .base import Problem, with_norm


def group_anagrams(strs):
    groups = {}
    for s in strs:
        groups.setdefault("".join(sorted(s)), []).append(s)
    return list(groups.values())


def _gen(rng):
    words = ["".join(rng.choice("abcd") for _ in range(rng.randint(0, 7))) for _ in range(30000)]
    return [[words]]


PROBLEM = Problem(
    id="group_anagrams",
    title="Group Anagrams",
    difficulty="medium",
    entry_point="group_anagrams",
    prompt=(
        "Group the strings in `strs` so that anagrams end up together. Return a list of groups "
        "(each a list of strings). The order of groups and the order inside a group do not matter. "
        "Duplicate strings must all be kept."
    ),
    starter="def group_anagrams(strs: list[str]) -> list[list[str]]:\n    ...",
    reference=group_anagrams,
    cases=[
        ([["eat", "tea", "tan", "ate", "nat", "bat"]], [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
        ([[""]], [[""]]),
        ([["a"]], [["a"]]),
        ([["ab", "ba", "abc"]], [["ab", "ba"], ["abc"]]),
        ([["a", "a", "b"]], [["a", "a"], ["b"]]),
        ([[]], []),
    ],
    gen_args=_gen,
    checker=with_norm(lambda g: sorted(sorted(x) for x in g)),
    tags=["hash-map", "string"],
)
