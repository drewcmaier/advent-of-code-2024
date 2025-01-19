from copy import deepcopy
from enum import Enum
import heapq

type Grid = list[list[str]]
type Point = tuple[int, int]
type Dim = tuple[int, int]


class Direction(Enum):
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    NORTH = (-1, 0)


def parse_input(f: str) -> tuple[Grid, Dim, Point, Point]:
    with open(f, "r") as file:
        lines = file.readlines()

    grid = [[c for c in line.strip()] for line in lines]
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "S":
                start = (i, j)
            elif col == "E":
                end = (i, j)

    dim = (len(grid), len(grid[0]))

    return (grid, dim, start, end)


def grid_str(grid: Grid, paths: list[tuple[set[Point], str]]) -> str:
    rows, cols = len(grid), len(grid[0])
    debug_grid = deepcopy(grid)

    for points, char in paths:
        for pi, pj in points:
            debug_grid[pi][pj] = char

    s = ""
    for i in range(rows):
        for j in range(cols):
            s += debug_grid[i][j]
        s += "\n"
    return s


def can_move_to(pos: Point, grid: Grid, dim: Dim) -> bool:
    in_bounds = 0 <= pos[0] < dim[0] and 0 <= pos[1] < dim[1]

    if not in_bounds:
        return False

    return grid[pos[0]][pos[1]] != "#"


def manhattan_dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos: Point, grid: Grid, dim: Dim) -> list[Point]:
    neighbors = []
    for d in Direction:
        d_pos = (d.value[0] + pos[0], d.value[1] + pos[1])
        if not can_move_to(d_pos, grid, dim):
            continue
        neighbors.append(d_pos)
    return neighbors


def a_star(
    grid: Grid, dim: Dim, start: Point, end: Point
) -> tuple[list[Point], dict[Point, int]]:
    open_set: tuple[int, Point] = []
    heapq.heappush(open_set, (0, start))

    came_from: dict[Point, Point] = {}
    g_score = {start: 0}
    f_score = {start: manhattan_dist(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path: list[Point] = []
            dist_to = {start: 0}
            path_len = len(came_from)
            i = 0
            while current in came_from:
                path.append(current)
                dist_to[current] = path_len - i
                current = came_from[current]
                i += 1
            path.append(start)
            return (path[::-1], dist_to)

        for neighbor in get_neighbors(current, grid, dim):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_dist(neighbor, end)

                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return ([], {})


# Get all points within Manhattan distance of current point
def points_within_range(start: Point, dist: int):
    s_i, s_j = start
    return set(
        {
            ((s_i + i, s_j + j), abs(i) + abs(j))
            for i in range(-dist, dist + 1)
            for j in range(-(dist - abs(i)), (dist - abs(i)) + 1)
        }
    )


def run_cheats(
    root: Point,
    path: list[Point],
    dist_to: dict[Point, int],
    max_len: int,
    min_delta: int,
):
    def find_cheat_points() -> set[Point]:
        point_len = dist_to[root]
        path_len = len(path)
        cheat_points: set[tuple[Point, int]] = set()

        for p, m_dist in points_within_range(root, max_len):
            if p in dist_to:
                start_to_p = dist_to[p]
                p_to_end = path_len - start_to_p
                cheat_len = point_len + p_to_end + m_dist
                savings = path_len - cheat_len

                if savings >= 0:
                    cheat_points.add((p, savings))

        return cheat_points

    over_min = 0
    cheat_points = find_cheat_points()

    for _, savings in cheat_points:
        if savings >= min_delta:
            over_min += 1

    return over_min


def part1():
    grid, dim, start, end = parse_input("input.txt")

    path, dist_to = a_star(grid, dim, start, end)

    return sum(run_cheats(p, path, dist_to, 2, 100) for p in path)


def part2():
    grid, dim, start, end = parse_input("input.txt")

    path, dist_to = a_star(grid, dim, start, end)

    total = sum(run_cheats(p, path, dist_to, 20, 100) for p in path)

    return total


print(f"Total: {part2()}")
