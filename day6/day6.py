from typing import List, Tuple
from enum import Enum
from copy import deepcopy

from os import system
from time import sleep

type Point = Tuple[int, int]
type Grid = List[str]


class Direction(Enum):
    EAST = (0, 1)
    WEST = (0, -1)
    SOUTH = (1, 0)
    NORTH = (-1, 0)


def parse_input():
    with open("input.txt", "r") as file:
        lines = file.readlines()

    grid = []
    for line in lines:
        row = []
        for c in line.strip():
            row.append(c)
        grid.append(row)

    return grid


def find_start(grid: Grid) -> Point | None:
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "^":
                return (i, j)

    return None


def in_bounds(pos: Point, grid: Grid) -> bool:
    rows, cols = len(grid), len(grid[0])
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols


def rotate_right(dir: Direction) -> Direction:
    if dir == Direction.EAST:
        return Direction.SOUTH
    elif dir == Direction.SOUTH:
        return Direction.WEST
    elif dir == Direction.WEST:
        return Direction.NORTH
    elif dir == Direction.NORTH:
        return Direction.EAST


def step(pos: Point, dir: Direction, grid: Grid) -> Tuple[Point, Direction, bool]:
    next_pos = (pos[0] + dir.value[0], pos[1] + dir.value[1])
    next_dir = dir

    # Turn right when hitting a wall
    turn_count = 0
    while (
        in_bounds(next_pos, grid)
        and grid[next_pos[0]][next_pos[1]] in ["#", "O"]
        and turn_count < 4
    ):
        next_dir = rotate_right(next_dir)
        next_pos = (pos[0] + next_dir.value[0], pos[1] + next_dir.value[1])
        turn_count += 1

    is_in_bounds = in_bounds(next_pos, grid)

    return [next_pos, next_dir, is_in_bounds]


def dir_string(dir: Direction) -> str:
    if dir == Direction.EAST:
        return ">"
    elif dir == Direction.WEST:
        return "<"
    elif dir == Direction.SOUTH:
        return "V"
    elif dir == Direction.NORTH:
        return "^"


def grid_string(grid: Grid):
    s = ""
    for row in grid:
        for col in row:
            s += col
        s += "\n"
    return s


def part1():
    grid = parse_input()

    pos, dir, can_continue = find_start(grid), Direction.NORTH, True
    next_grid = deepcopy(grid)

    while can_continue:
        prev_pos = pos
        pos, dir, can_continue = step(pos, dir, grid)

        next_grid[prev_pos[0]][prev_pos[1]] = "X"
        if can_continue:
            next_grid[pos[0]][pos[1]] = dir_string(dir)

        # Crude animation
        # system("clear")
        # print(grid_string(next_grid))
        # sleep(0.1)

    def count_visited():
        count = 0
        for row in next_grid:
            for col in row:
                if col == "X":
                    count += 1
        return count

    return (next_grid, count_visited())


def part2():
    grid = parse_input()
    rows, cols = len(grid), len(grid[0])

    # Get all points the guard will visit
    all_visited = []
    base_case = part1()
    for i in range(rows):
        for j in range(cols):
            if base_case[0][i][j] == "X" and grid[i][j] == ".":
                all_visited.append((i, j))

    start_pos = find_start(grid)
    loop_count = 0

    # Insert obstruction along path and look for a loop
    for i, j in all_visited:
        test_grid = deepcopy(grid)
        test_grid[i][j] = "O"

        pos, dir, can_continue = start_pos, Direction.NORTH, True
        next_grid = deepcopy(test_grid)

        visited = set()
        while can_continue:
            # A loop occurs when the same position and orientation have been visited
            if (pos[0], pos[1], dir) in visited:
                loop_count += 1
                # print(grid_string(test_grid))
                break

            visited.add((pos[0], pos[1], dir))

            pos, dir, can_continue = step(pos, dir, test_grid)

    return loop_count


part2()
