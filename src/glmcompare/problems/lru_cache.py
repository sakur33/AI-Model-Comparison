from .base import Problem


def run_lru_cache(capacity, operations):
    from collections import OrderedDict

    cache, out = OrderedDict(), []
    for op in operations:
        if op[0] == "get":
            if op[1] in cache:
                cache.move_to_end(op[1])
                out.append(cache[op[1]])
            else:
                out.append(-1)
        else:
            _, k, v = op
            cache[k] = v
            cache.move_to_end(k)
            if len(cache) > capacity:
                cache.popitem(last=False)
    return out


def _gen(rng):
    def mk(n, cap_keys):
        ops = []
        for _ in range(n):
            k = rng.randint(0, cap_keys)
            ops.append(["put", k, rng.randint(0, 10**6)] if rng.random() < 0.4 else ["get", k])
        return ops
    return [[100, mk(200000, 1000)], [1, mk(1000, 5)], [5000, mk(200000, 6000)]]


PROBLEM = Problem(
    id="lru_cache",
    title="LRU Cache Simulation",
    difficulty="medium",
    entry_point="run_lru_cache",
    prompt=(
        "Simulate a Least-Recently-Used cache with the given `capacity` (>= 1). `operations` is a list "
        "of `[\"put\", key, value]` and `[\"get\", key]`. `get` returns the value or -1 if absent, and "
        "marks the key as most recently used. `put` inserts or updates a key (also marking it most "
        "recently used); if the size then exceeds `capacity`, evict the least recently used key. "
        "Return the list of results of the `get` operations, in order. Both operations must be O(1) "
        "on average (there can be 200,000 operations)."
    ),
    starter="def run_lru_cache(capacity: int, operations: list[list]) -> list[int]:\n    ...",
    reference=run_lru_cache,
    cases=[
        ([2, [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2], ["put", 4, 4],
              ["get", 1], ["get", 3], ["get", 4]]], [1, -1, -1, 3, 4]),
        ([1, [["put", 2, 1], ["get", 2], ["put", 3, 2], ["get", 2], ["get", 3]]], [1, -1, 2]),
        ([2, [["put", 1, 1], ["put", 2, 2], ["put", 1, 10], ["put", 3, 3], ["get", 2], ["get", 1], ["get", 3]]],
         [-1, 10, 3]),
        ([3, []], []),
    ],
    gen_args=_gen,
    tags=["design", "hash-map", "linked-list"],
)
