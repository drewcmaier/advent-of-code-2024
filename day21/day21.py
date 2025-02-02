from enum import Enum
from functools import cache
from paths import (
    min_numpad_paths,
    numpad_start_point,
    numpad_locations,
    min_directional_paths,
    directional_start_point,
    directional_locations,
)

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
    numpad_paths: dict[Point, dict[Point, list[Move]]],
    numpad_start_point: Point,
    numpad_locations: dict[str, Point],
    directional_paths: dict[Point, dict[Point, list[Move]]],
    directional_start_point: Point,
    directional_locations: dict[str, Point],
    dbg: bool = False,
):
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

    return sum(complexity)


def part1():
    complexity = simulate(
        2,
        min_numpad_paths,
        numpad_start_point,
        numpad_locations,
        min_directional_paths,
        directional_start_point,
        directional_locations,
        dbg=False,
    )
    return complexity


def part2():
    complexity = simulate(
        25,
        min_numpad_paths,
        numpad_start_point,
        numpad_locations,
        min_directional_paths,
        directional_start_point,
        directional_locations,
        dbg=False,
    )
    return complexity
