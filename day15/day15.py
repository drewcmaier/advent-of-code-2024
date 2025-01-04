from enum import Enum
from vector2d import Vector2D
from copy import deepcopy
from os import system
from time import sleep

type Grid = list[list[str]]


class Tile(Enum):
    ROBOT = "@"
    WALL = "#"
    BOX = "O"
    BOX_LEFT = "["
    BOX_RIGHT = "]"
    EMPTY = "."


class RobotState:
    def __init__(self, pos: Vector2D, dir: Vector2D):
        self.pos = pos
        self.dir = dir

    def __repr__(self):
        return f"{self.pos}, {self.dir}, {self.length}"


def parse_input(f: str) -> tuple[Grid, list[tuple[str, Vector2D]]]:
    with open(f, "r") as file:
        text = file.read()

    def move_dir(move: str) -> Vector2D:
        match move:
            case ">":
                return Vector2D(1, 0)
            case "<":
                return Vector2D(-1, 0)
            case "v":
                return Vector2D(0, 1)
            case "^":
                return Vector2D(0, -1)

    map_str, move_str = text.split("\n\n")

    map: Grid = [[c for c in line.strip()] for line in map_str.split()]
    moves: list[Vector2D] = []
    for m in move_str.strip():
        move = move_dir(m)
        if move is not None:
            moves.append((m, move))

    return (map, moves)


def map_str(map: Grid):
    rows, cols = len(map), len(map[0])
    s = ""
    for i in range(rows):
        for j in range(cols):
            s += map[i][j]
        s += "\n"
    return s


def in_bounds(pos: Vector2D, map: Grid) -> bool:
    rows, cols = len(map), len(map[0])
    if not (0 <= pos.y < rows and 0 <= pos.x < cols):
        return False

    tile = map[pos.y][pos.x]
    if tile == Tile.WALL.value:
        return False

    return True


def find_start(map: Grid) -> Vector2D | None:
    rows, cols = len(map), len(map[0])
    for i in range(rows):
        for j in range(cols):
            if map[i][j] == Tile.ROBOT.value:
                return Vector2D(j, i)

    return None


def apply_move(move: Vector2D, state: RobotState, map: Grid) -> tuple[RobotState, Grid]:
    next_map = deepcopy(map)
    next_state = deepcopy(state)

    next_state.pos = state.pos + move
    next_state.dir = move

    visited: set[Vector2D] = set()
    group_tiles: list[Vector2D] = []

    bfs = [state.pos]
    while len(bfs) > 0:
        test_pos = bfs.pop(0)

        if test_pos in visited:
            continue

        tile = map[test_pos.y][test_pos.x]
        is_box, is_box_left, is_box_right, is_robot = (
            tile == Tile.BOX.value,
            tile == Tile.BOX_LEFT.value,
            tile == Tile.BOX_RIGHT.value,
            tile == Tile.ROBOT.value,
        )

        if not (is_box or is_box_left or is_box_right or is_robot):
            continue

        group_tiles.append(test_pos)
        visited.add(test_pos)

        # Start BFS in direction of movement next to robot
        if is_robot:
            bfs.append(test_pos + next_state.dir)
            continue

        # For a box, check if there is another box adjacent to this point in the movement direction.
        # If so, add that box and test from its extents next.
        bfs.append(test_pos + next_state.dir)

        # Also check the other side of the current box to search for other adjacent boxes.
        if is_box_left or is_box_right:
            next_side_dir = Vector2D(1 if is_box_left else -1, 0)
            bfs.append(test_pos + next_side_dir)

    # Check for boundary collision. If hit, roll back
    for t in group_tiles:
        if not in_bounds(t + next_state.dir, map):
            return (state, map)

    # Clear previous cells
    for t in group_tiles:
        next_map[t.y][t.x] = Tile.EMPTY.value

    # Move cells in grid to new position
    for t in group_tiles:
        dest_pos = t + next_state.dir
        next_map[dest_pos.y][dest_pos.x] = map[t.y][t.x]

    return (next_state, next_map)


def calculate_box_gps_sum(map: Grid) -> int:
    rows, cols = len(map), len(map[0])
    gps_sum = 0
    for i in range(rows):
        for j in range(cols):
            if map[i][j] in [Tile.BOX.value, Tile.BOX_LEFT.value]:
                gps_score = 100 * i + j
                gps_sum += gps_score
    return gps_sum


def widen_map(map: Grid) -> Grid:
    rows, cols = len(map), len(map[0])
    wide_map = []
    for row in range(rows):
        wide_row = []
        for col in range(cols):
            tile = map[row][col]
            match tile:
                case "#":
                    wide_row.extend(["#", "#"])
                case "O":
                    wide_row.extend(["[", "]"])
                case ".":
                    wide_row.extend([".", "."])
                case "@":
                    wide_row.extend(["@", "."])
        wide_map.append(wide_row)

    return wide_map


def part1():
    map, moves = parse_input("input.txt")
    print(f"Start\n{map_str(map)}")

    pos = find_start(map)
    state = RobotState(pos, Vector2D(0, 0))
    while len(moves) > 0:
        c, move = moves.pop(0)
        state, map = apply_move(move, state, map)

        # ANIM_DELAY = 0.1
        # system("clear")
        # print(c)
        # print(state)
        # print(map_str(map))
        # sleep(ANIM_DELAY)

    print(f"End\n{map_str(map)}")
    gps_sum = calculate_box_gps_sum(map)
    return gps_sum


def part2():
    map, moves = parse_input("test2.txt")
    map = widen_map(map)
    print(f"Start\n{map_str(map)}")

    pos = find_start(map)
    state = RobotState(pos, Vector2D(0, 0))
    while len(moves) > 0:
        c, move = moves.pop(0)
        state, map = apply_move(move, state, map)

        # ANIM_DELAY = 0.03
        # system("clear")
        # print(c)
        # print(state)
        # print(map_str(map))
        # sleep(ANIM_DELAY)

    print(f"End\n{map_str(map)}")
    gps_sum = calculate_box_gps_sum(map)
    return gps_sum


print(part2())
