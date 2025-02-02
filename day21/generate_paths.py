import heapq
from copy import deepcopy
from itertools import permutations
from day21 import (
    Point,
    Grid,
    Move,
    Direction,
    EMPTY,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    TURN,
    NUMERIC_BUTTONS,
    DIRECTIONAL_BUTTONS,
    simulate,
)


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


def get_button_locations(grid: Grid):
    locations = dict[str, Point]()
    for i, _ in enumerate(grid):
        for j, button in enumerate(grid[i]):
            locations[button] = (i, j)
    return locations


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

            # Store path with fewest turns
            for other_point, path in paths_from_point.items():
                if point in prev_paths and num_turns(
                    prev_paths[point][other_point]
                ) < num_turns(path):
                    paths_from_point[other_point] = prev_paths[point][other_point]

            paths[point] = paths_from_point

    return paths


# Precompute min paths and points of interest.
# Run this and dump the contents to files so we don't need to
# recalculate every time.
def find_minimal_paths(iterations: int):
    min_numpad_paths, min_directional_paths = {}, {}
    min_complexity = float("inf")

    numpad_paths = {}
    numpad_locations = get_button_locations(NUMERIC_BUTTONS)
    numpad_start_point = numpad_locations["A"]

    directional_paths = {}
    directional_locations = get_button_locations(DIRECTIONAL_BUTTONS)
    directional_start_point = directional_locations["A"]

    # Tune Dijkstra parameters to find min paths
    for l, r, d, u, t in permutations(range(10), 5):
        costs = {LEFT: l, RIGHT: r, UP: u, DOWN: d, TURN: t}

        numpad_paths = precompute_paths(NUMERIC_BUTTONS, costs, numpad_paths)
        directional_paths = precompute_paths(
            DIRECTIONAL_BUTTONS, costs, directional_paths
        )
        complexity = simulate(
            iterations,
            numpad_paths,
            numpad_start_point,
            numpad_locations,
            directional_paths,
            directional_start_point,
            directional_locations,
        )

        if complexity < min_complexity:
            min_numpad_paths = deepcopy(numpad_paths)
            min_directional_paths = deepcopy(directional_paths)
            min_complexity = complexity
            print("Min complexity", min_complexity)

    return (
        min_numpad_paths,
        numpad_locations,
        numpad_start_point,
        min_directional_paths,
        directional_locations,
        directional_start_point,
    )


def generate_min_path_file(iterations: int):
    (
        min_numpad_paths,
        numpad_locations,
        numpad_start_point,
        min_directional_paths,
        directional_locations,
        directional_start_point,
    ) = find_minimal_paths(iterations)

    with open("paths.py", "w") as file:
        file.write(f"min_numpad_paths = {min_numpad_paths}\n")
        file.write(f"numpad_locations = {numpad_locations}\n")
        file.write(f"numpad_start_point = {numpad_start_point}\n")
        file.write(f"min_directional_paths = {min_directional_paths}\n")
        file.write(f"directional_locations = {directional_locations}\n")
        file.write(f"directional_start_point = {directional_start_point}\n")


# Tune this number to get optimal paths
generate_min_path_file(5)
