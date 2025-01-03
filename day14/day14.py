import re
import numpy as np
from numpy.typing import ArrayLike, NDArray

type RobotState = tuple[ArrayLike, ArrayLike]
type Grid = NDArray


def parse_input(f: str):
    with open(f, "r") as file:
        lines = file.readlines()

    robot_states: list[RobotState] = []
    robot_pattern = re.compile(r"p=(-?\d+,-?\d+)\s+v=(-?\d+,-?\d+)")

    for line in lines:
        match = robot_pattern.match(line)
        p, v = match.groups()
        p_arr, v_arr = np.fromstring(p, sep=",", dtype=np.int32), np.fromstring(
            v, sep=",", dtype=np.int32
        )
        robot_states.append((p_arr, v_arr))

    return robot_states


def step(robot_states: list[RobotState], grid: Grid):
    next_grid = np.copy(grid)
    height, width = grid.shape
    for r in range(len(robot_states)):
        p, v = robot_states[r]
        px, py = p

        next_grid[py][px] -= 1

        next_p = np.mod(p + v, (width, height))
        next_grid[next_p[1]][next_p[0]] += 1

        robot_states[r] = (next_p, v)

    return next_grid


def compute_safety_factor(grid: Grid) -> int:
    rows, cols = grid.shape
    row_center = rows // 2
    col_center = cols // 2

    top_left = grid[:row_center, :col_center]
    top_right = grid[:row_center, col_center + 1 :]
    bottom_left = grid[row_center + 1 :, :col_center]
    bottom_right = grid[row_center + 1 :, col_center + 1 :]

    sum_top_left = np.sum(top_left)
    sum_top_right = np.sum(top_right)
    sum_bottom_left = np.sum(bottom_left)
    sum_bottom_right = np.sum(bottom_right)

    return sum_top_left * sum_top_right * sum_bottom_left * sum_bottom_right


def part1():
    # config = ("test.txt", (7, 11))
    config = ("input.txt", (103, 101))

    robot_states = parse_input(config[0])
    grid = np.zeros(config[1], dtype=np.int64)

    # initialize grid
    for robot in robot_states:
        px, py = robot[0]
        grid[py][px] += 1

    # iterate
    for _ in range(100):
        grid = step(robot_states, grid)

    return compute_safety_factor(grid)


def print_grid(grid: Grid):
    rows, cols = grid.shape
    s = ""
    for i in range(rows):
        for j in range(cols):
            s += "█" if grid[i][j] != 0 else "."
        s += "\n"
    print(s)


def middle_percent(grid: Grid) -> float:
    rows, cols = grid.shape
    row_center = rows // 2
    col_center = cols // 2

    middle = grid[
        row_center - row_center // 2 : row_center + row_center // 2,
        col_center - col_center // 2 : col_center + col_center // 2,
    ]

    return np.sum(middle) / middle.size


def part2():
    config = ("input.txt", (103, 101))

    max_percent = (0.0, 0)
    for _ in range(2):
        robot_states = parse_input(config[0])
        grid = np.zeros(config[1], dtype=np.int64)

        # Initialize grid
        for robot in robot_states:
            px, py = robot[0]
            grid[py][px] += 1

        if max_percent[1] == 0:
            # Find highest concentration in the middle of the image, assuming the tree is there
            for i in range(10000):
                grid = step(robot_states, grid)
                pct = middle_percent(grid)
                if pct > max_percent[0]:
                    max_percent = (pct, i + 1)
            print(max_percent)
        else:
            for _ in range(max_percent[1]):
                grid = step(robot_states, grid)
            print_grid(grid)
