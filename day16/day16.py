import heapq
from collections import defaultdict
from enum import Enum


class Direction(Enum):
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    NORTH = (-1, 0)

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value[0] < other.value[0] and self.value[1] < other.value[1]


type Grid = list[list[str]]
type Point = tuple[int, int]
type CellState = tuple[Point, Direction]


def parse_input(f: str) -> tuple[Grid, Point, Point]:
    with open(f, "r") as file:
        lines = file.readlines()

    grid = [[c for c in line.strip()] for line in lines]
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "S":
                start = (i, j)
            elif col == "E":
                end = (i, j)

    return (grid, start, end)


def grid_str(grid: Grid, path: set[Point]):
    rows, cols = len(grid), len(grid[0])
    s = ""
    for i in range(rows):
        for j in range(cols):
            s += grid[i][j] if (i, j) not in path else "█"
        s += "\n"
    return s


def can_move_to(grid: Grid, pos: Point) -> bool:
    rows, cols = len(grid), len(grid[0])
    if not (0 <= pos[0] < rows and 0 <= pos[1] < cols):
        return False

    return grid[pos[0]][pos[1]] != "#"


def get_neighbors(grid: Grid, pos: Point) -> list[CellState]:
    neighbors = []
    for d in Direction:
        d_pos = (d.value[0] + pos[0], d.value[1] + pos[1])
        if not can_move_to(grid, d_pos):
            continue
        neighbors.append((d_pos, d))
    return neighbors


def find_path(
    grid: Grid, start: Point, end: Point, initial_heading: Direction
) -> tuple[int, set[Point]]:
    # Dijkstra's algorithm
    visited: set[Point] = set()
    q = [(0, start, initial_heading, {start})]
    while q:
        score, pos, heading, path = heapq.heappop(q)

        if pos in visited:
            continue

        visited.add(pos)

        # system("clear")
        # print(grid_str(grid, path))
        # sleep(0.03)

        if pos == end:
            return (score, path)

        for neighbor, direction in get_neighbors(grid, pos):
            pos_score = 1 if direction == heading else 1001
            heapq.heappush(
                q, (score + pos_score, neighbor, direction, path | {neighbor})
            )

    return (0, {})


def part1():
    grid, start, end = parse_input("input.txt")
    score, path = find_path(grid, start, end, Direction.EAST)

    print(grid_str(grid, path))

    return score


def find_all_shortest_path_nodes(
    grid: Grid, start: Point, end: Point, initial_heading: Direction
) -> set[Point]:
    min_scores: dict[CellState, int] = defaultdict()
    parent_states: dict[CellState, set[CellState]] = defaultdict(set)

    q = [(0, (start, initial_heading))]
    while q:
        score, cur_state = heapq.heappop(q)
        pos, heading = cur_state

        for neighbor in get_neighbors(grid, pos):
            neighbor_direction = neighbor[1]
            direction_score = 1 if neighbor_direction == heading else 1001
            neighbor_score = score + direction_score

            if neighbor_score < min_scores.get(neighbor, float("inf")):
                min_scores[neighbor] = neighbor_score
                parent_states[neighbor] = {cur_state}
                heapq.heappush(
                    q,
                    (neighbor_score, neighbor),
                )
            elif neighbor_score == min_scores.get(neighbor):
                parent_states[neighbor].add(cur_state)

    end_state = (end, Direction.NORTH)
    reverse_dfs = [(end_state, [end_state[0]])]
    all_paths: list[list[Point]] = []
    while reverse_dfs:
        state, path = reverse_dfs.pop()
        parents = parent_states.get(state, [])
        if not parents:
            all_paths.append(path)
        else:
            reverse_dfs.extend((parent, path + [parent[0]]) for parent in parents)

    unique_points = {point for path in all_paths for point in path}
    return unique_points


def part2():
    grid, start, end = parse_input("test.txt")

    all_points = find_all_shortest_path_nodes(grid, start, end, Direction.EAST)

    return len(all_points)
