from enum import Enum
import heapq

type Grid = list[list[str]]
type Point = tuple[int, int]


class Direction(Enum):
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    NORTH = (-1, 0)


def parse_input(f) -> Grid:
    with open(f, "r") as file:
        lines = file.readlines()

    positions: list[Point] = []
    for line in lines:
        x, y = line.strip().split(",")
        positions.append((int(x), int(y)))

    return positions


def grid_str(grid: Grid, path: set[Point]):
    rows, cols = len(grid), len(grid[0])
    s = ""
    for i in range(rows):
        for j in range(cols):
            s += grid[i][j] if (i, j) not in path else "O"
        s += "\n"
    return s


def can_move_to(pos: Point, grid: Grid) -> bool:
    rows, cols = len(grid), len(grid[0])

    if not (0 <= pos[0] < rows and 0 <= pos[1] < cols):
        return False

    return grid[pos[0]][pos[1]] != "#"


def heuristic(a: Point, b: Point) -> int:
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(grid: Grid, pos: Point) -> list[Point]:
    neighbors = []
    for d in Direction:
        d_pos = (d.value[0] + pos[0], d.value[1] + pos[1])
        if not can_move_to(d_pos, grid):
            continue
        neighbors.append(d_pos)
    return neighbors


def a_star(grid: Grid, start: Point, end: Point) -> list[Point]:
    open_set: tuple[int, Point] = []
    heapq.heappush(open_set, (0, start))

    came_from: dict[Point, Point] = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path: list[Point] = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(grid, current):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)

                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


def part1():
    # dim, num_bytes, f = (6, 12, "test.txt")
    dim, num_bytes, f = (70, 1024, "input.txt")
    grid = [["." for _ in range(dim + 1)] for _ in range(dim + 1)]
    positions = parse_input(f)

    for i, (x, y) in enumerate(positions):
        if i < num_bytes:
            grid[y][x] = "#"

    path = a_star(grid, (0, 0), (dim, dim))

    print(grid_str(grid, path))

    return len(path) - 1


def part2():
    # dim, f = (6, "test.txt")
    dim, f = (70, "input.txt")
    grid = [["." for _ in range(dim + 1)] for _ in range(dim + 1)]
    positions = parse_input(f)

    # Slightly better than brute force. See if incoming bytes
    # were on the previous path. If not, the last path is still valid
    prev_path = []
    for x, y in positions:
        grid[y][x] = "#"
        if not prev_path or (y, x) in prev_path:
            path = a_star(grid, (0, 0), (dim, dim))
            if len(path) == 0:
                return (x, y)
            prev_path = path

    return None
