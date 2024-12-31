import functools
from copy import deepcopy
from typing import List


def parse_input(f):
    with open(f, "r") as file:
        input = file.readline()

    arrangement = [int(n) for n in input.split()]
    return arrangement


@functools.cache
def apply_rules(stone: int) -> List[int]:
    if stone == 0:
        return [1]

    stone_str = str(stone)
    num_digits = len(stone_str)
    if num_digits % 2 == 0:
        half_digits = int(num_digits / 2)
        left, right = stone_str[:half_digits], stone_str[half_digits:]
        return [int(left), int(right)]

    return [stone * 2024]


def blink(arrangement: List[int]):
    next_arrangement = []
    for stone in arrangement:
        next_stones = apply_rules(stone)
        next_arrangement.extend(next_stones)
    return next_arrangement


def part1():
    input = parse_input("input.txt")

    arrangement = deepcopy(input)
    for _ in range(25):
        arrangement = blink(arrangement)

    print(len(arrangement))


@functools.cache
def num_stones(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone == 0:
        return num_stones(1, blinks - 1)

    stone_str = str(stone)
    num_digits = len(stone_str)

    if num_digits % 2 == 0:
        half_digits = int(num_digits / 2)
        left, right = int(stone_str[:half_digits]), int(stone_str[half_digits:])
        return num_stones(left, blinks - 1) + num_stones(right, blinks - 1)

    return num_stones(2024 * stone, blinks - 1)


def part2():
    input = parse_input("input.txt")

    l = sum(num_stones(stone, 75) for stone in input)

    print(l)


part1()
part2()
