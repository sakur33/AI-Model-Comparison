from .base import Problem


def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1
                seen[r][c] = True
                stack = [(r, c)]
                while stack:
                    y, x = stack.pop()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == "1" and not seen[ny][nx]:
                            seen[ny][nx] = True
                            stack.append((ny, nx))
    return count


def _gen(rng):
    def mk(h, w, p):
        return ["".join("1" if rng.random() < p else "0" for _ in range(w)) for _ in range(h)]
    return [[mk(50, 50, 0.45)], [mk(200, 200, 0.5)], [["1" * 60] * 60], [mk(30, 80, 0.2)]]


PROBLEM = Problem(
    id="number_of_islands",
    title="Number of Islands",
    difficulty="medium",
    entry_point="num_islands",
    prompt=(
        "`grid` is a list of equal-length strings made of '1' (land) and '0' (water). Count the "
        "islands. An island is a maximal group of land cells connected horizontally or vertically "
        "(not diagonally). The grid may be empty. Grids can be fully land and up to 200x200."
    ),
    starter="def num_islands(grid: list[str]) -> int:\n    ...",
    reference=num_islands,
    cases=[
        ([["11110", "11010", "11000", "00000"]], 1),
        ([["11000", "11000", "00100", "00011"]], 3),
        ([["1"]], 1), ([["0"]], 0), ([["101", "010", "101"]], 5), ([[]], 0),
    ],
    gen_args=_gen,
    tags=["graph", "dfs", "grid"],
)
