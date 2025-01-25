import heapq
from enum import Enum
from functools import cache
from itertools import permutations

type Point = tuple[int, int]
type Grid = list[list[str]]
type Move = tuple[Point, str]


EMPTY = "."
ACTIVATE = "A"
UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"
TURN = "T"


class Direction(Enum):
    UP = ((-1, 0), UP)
    DOWN = ((1, 0), DOWN)
    LEFT = ((0, -1), LEFT)
    RIGHT = ((0, 1), RIGHT)


NUMERIC_BUTTONS = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [EMPTY, "0", ACTIVATE],
]
DIRECTIONAL_BUTTONS = [
    [EMPTY, UP, ACTIVATE],
    [LEFT, DOWN, RIGHT],
]


def parse_input(f: str):
    with open(f, "r") as file:
        lines = file.readlines()

    return [line.strip() for line in lines]


def get_button_locations(grid: Grid):
    locations = dict[str, Point]()
    for i, _ in enumerate(grid):
        for j, button in enumerate(grid[i]):
            locations[button] = (i, j)
    return locations


def can_move_to(pos: Point, grid: Grid) -> bool:
    rows, cols = len(grid), len(grid[0])
    if not (0 <= pos[0] < rows and 0 <= pos[1] < cols):
        return False

    return grid[pos[0]][pos[1]] != EMPTY


def find_paths(start: Point, grid: Grid, costs: dict[str, int]):
    def get_neighbors(p: Point):
        neighbors: list[Move] = []
        for d in Direction:
            offset, symbol = d.value
            d_pos = (offset[0] + p[0], offset[1] + p[1])
            if not can_move_to(d_pos, grid):
                continue
            neighbors.append((d_pos, symbol))
        return neighbors

    # Dijkstra's algorithm
    distances: dict[Point, int] = {start: 0}
    paths: dict[Point, list[Move]] = {start: []}
    q = [(0, start, "", [(start, "")])]
    while q:
        dist, pos, direction, path = heapq.heappop(q)

        for neighbor in get_neighbors(pos):
            neighbor_point, neighbor_direction = neighbor
            neighbor_path = path + [(neighbor_point, neighbor_direction)]

            turn_cost = (
                costs[TURN] if direction and direction != neighbor_direction else 0
            )

            neighbor_cost = costs[neighbor_direction]
            neighbor_score = dist + 1 + turn_cost + neighbor_cost

            if neighbor_score < distances.get(neighbor_point, float("inf")):
                distances[neighbor_point] = neighbor_score
                paths[neighbor_point] = neighbor_path
                heapq.heappush(
                    q,
                    (
                        neighbor_score,
                        neighbor_point,
                        neighbor_direction,
                        neighbor_path,
                    ),
                )

    return paths


def precompute_paths(
    grid: Grid, costs: dict[str, int], prev_paths: dict[Point, dict[Point, list[Move]]]
):
    def num_turns(moves: list[Move]):
        turns, heading = 0, ""
        for move in moves:
            _, d = move
            if d != heading:
                turns += 1
            heading = d
        return turns

    # For each point, generate path to all other points
    paths = prev_paths
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == EMPTY:
                continue

            point = (i, j)
            paths_from_point = find_paths(point, grid, costs)
            for other_point, path in paths_from_point.items():
                if point in prev_paths and num_turns(
                    prev_paths[point][other_point]
                ) < num_turns(path):
                    paths_from_point[other_point] = prev_paths[point][other_point]

            paths[point] = paths_from_point

    return paths


def debug_move(move: list[Move], grid: Grid):
    s = ""
    rows, cols = len(grid), len(grid[0])
    moves = dict[Point, str]()
    for point, symbol in move:
        moves[point] = symbol

    for i in range(rows):
        for j in range(cols):
            s += grid[i][j] if (i, j) not in moves else "█"
        s += "\n"
    return s


def debug_enter_buttons(buttons: str, start: Point, grid: Grid):
    button_lookup = {}
    for d in Direction:
        direction, symbol = d.value
        button_lookup[symbol] = direction
    button_lookup[ACTIVATE] = ACTIVATE

    s = ""
    cur = start
    for b in buttons:
        if b == ACTIVATE:
            s += grid[p[0]][p[1]]
        else:
            direction = button_lookup[b]
            p = (cur[0] + direction[0], cur[1] + direction[1])
            cur = p

    return s


def path_str(path: list[Move]):
    return "".join(symbol for _, symbol in path if symbol)


def button_path(
    buttons: str,
    start: Point,
    button_paths: dict[Point, dict[Point, list[Move]]],
    button_locations: dict[str, Point],
    max_depth: int,
):
    @cache
    def recurse(btns: str, depth: int):
        if depth == 0:
            return btns

        result = ""

        prev_pos = start
        for b in btns:
            pos = button_locations[b]
            path = f"{path_str(button_paths[prev_pos][pos])}A"
            result += recurse(path, depth - 1)
            prev_pos = pos

        return result

    return recurse(buttons, max_depth)


def button_path_length(
    buttons: str,
    start: Point,
    button_paths: dict[Point, dict[Point, list[Move]]],
    button_locations: dict[str, Point],
    max_depth: int,
):
    @cache
    def recurse(btns: str, depth: int):
        if depth == 0:
            return len(btns)

        result = 0

        prev_pos = start
        for b in btns:
            pos = button_locations[b]
            path = f"{path_str(button_paths[prev_pos][pos])}A"
            result += recurse(path, depth - 1)
            prev_pos = pos

        return result

    return recurse(buttons, max_depth)


def simulate(
    iterations: int,
    costs: dict[str, int] = {},
    min_numpad_path: dict[Point, dict[Point, list[Move]]] = {},
    min_directional_path: dict[Point, dict[Point, list[Move]]] = {},
    dbg: bool = False,
):
    numpad_paths = precompute_paths(NUMERIC_BUTTONS, costs, min_numpad_path)
    numpad_locations = get_button_locations(NUMERIC_BUTTONS)
    numpad_start_point = numpad_locations["A"]

    directional_paths = precompute_paths(
        DIRECTIONAL_BUTTONS, costs, min_directional_path
    )
    directional_locations = get_button_locations(DIRECTIONAL_BUTTONS)
    directional_start_point = directional_locations["A"]

    complexity = []
    numpad_instructions = parse_input("test.txt" if dbg else "input.txt")
    directional_instructions: list[str] = []
    for instruction in numpad_instructions:
        complexity.append(int(instruction[:-1]))
        path = button_path(
            instruction, numpad_start_point, numpad_paths, numpad_locations, 1
        )
        directional_instructions.append(path)

    for i, instruction in enumerate(directional_instructions):
        path = instruction
        length = button_path_length(
            path,
            directional_start_point,
            directional_paths,
            directional_locations,
            iterations,
        )
        complexity[i] *= length

    return (sum(complexity), numpad_paths, directional_paths)


def part1(iterations: int):
    numpad_paths, directional_paths = {}, {}
    min_complexity, min_params = float("inf"), {}

    # Tune Dijkstra parameters to find min paths
    for d, u, t in permutations(range(10), 3):
        params = {LEFT: 1, RIGHT: 3, UP: u, DOWN: d, TURN: t}
        complexity, numpad_paths, directional_paths = simulate(
            iterations, params, numpad_paths, directional_paths
        )
        if complexity < min_complexity:
            min_complexity = complexity
            min_params = params

    # print(numpad_paths)
    # print(directional_paths)

    simulate(iterations, min_params, numpad_paths, directional_paths, dbg=False)
    print(f"Answer: {min_complexity}")
    return (min_params, numpad_paths, directional_paths)


def part2():
    return part1(25)


part2()
