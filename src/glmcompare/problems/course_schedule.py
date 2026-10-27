from .base import Problem


def can_finish(num_courses, prerequisites):
    from collections import deque

    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return done == num_courses


def _gen(rng):
    n = 3000
    chain = [[i + 1, i] for i in range(n - 1)]
    cyc = chain + [[0, n - 1]]
    m = 20000
    dag = []
    for _ in range(60000):
        a, b = rng.sample(range(m), 2)
        dag.append([max(a, b), min(a, b)])  # edges go low -> high, so acyclic
    bad = dag + [[5, 17000], [17000, 5]]
    return [[n, chain], [n, cyc], [m, dag], [m, bad]]


PROBLEM = Problem(
    id="course_schedule",
    title="Course Schedule",
    difficulty="medium",
    entry_point="can_finish",
    prompt=(
        "There are `num_courses` courses labelled `0..num_courses-1`. Each pair `[a, b]` in "
        "`prerequisites` means you must take course `b` before course `a`. Return `True` if it is "
        "possible to finish all courses (i.e. the dependency graph has no cycle). A pair `[x, x]` "
        "is a cycle. Graphs can have 20,000 nodes and long dependency chains."
    ),
    starter="def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:\n    ...",
    reference=can_finish,
    cases=[
        ([2, [[1, 0]]], True),
        ([2, [[1, 0], [0, 1]]], False),
        ([1, []], True),
        ([3, [[1, 0], [2, 1]]], True),
        ([3, [[1, 0], [2, 1], [0, 2]]], False),
        ([4, [[1, 0], [2, 0], [3, 1], [3, 2]]], True),
        ([2, [[0, 0]]], False),
    ],
    gen_args=_gen,
    tags=["graph", "topological-sort"],
)
