from .base import Problem


def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        else:
            stack.append(c)
    return not stack


def _gen(rng):
    cases = [["()" * 50000], ["(" * 50000 + ")" * 49999]]
    for _ in range(40):
        cases.append(["".join(rng.choice("()[]{}") for _ in range(rng.randint(1, 24)))])
    return cases


PROBLEM = Problem(
    id="valid_parentheses",
    title="Valid Parentheses",
    difficulty="easy",
    entry_point="is_valid",
    prompt=(
        "Given a string `s` made only of the characters `()[]{}`, return `True` if every bracket is "
        "closed by the same type of bracket and in the correct order, otherwise `False`. "
        "The empty string is valid."
    ),
    starter="def is_valid(s: str) -> bool:\n    ...",
    reference=is_valid,
    cases=[
        (["()"], True), (["()[]{}"], True), (["(]"], False), (["([)]"], False),
        (["{[]}"], True), ([""], True), (["(("], False), (["]"], False),
    ],
    gen_args=_gen,
    tags=["stack", "string"],
)
