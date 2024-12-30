from copy import deepcopy
from enum import Enum
from typing import List, Tuple

type Grid = List[List[int]]
type Location = Tuple[int, int]


def debug_path(map, path):
    def map_str(map: Grid):
        s = ""
        for row in map:
            for col in row:
                s += str(col)
            s += "\n"
        return s

    path_map = [["." for _ in r] for r in map]
    for i, p in enumerate(path):
        path_map[p[0]][p[1]] = map[p[0]][p[1]]
    print(map_str(path_map))


def parse_input(f) -> Grid:
    with open(f, "r") as file:
        lines = file.readlines()

    map = [[int(c) if c != "." else -1 for c in line.strip()] for line in lines]
    return map


def in_bounds(loc: Location, grid: Grid) -> bool:
    rows, cols = len(grid), len(grid[0])
    return 0 <= loc[0] < rows and 0 <= loc[1] < cols


def find_trailheads(map: Grid) -> List[Location]:
    trailheads: List[Location] = []

    rows, cols = len(map), len(map[0])
    for i in range(rows):
        for j in range(cols):
            if map[i][j] == 0:
                trailheads.append((i, j))

    return trailheads


def trailhead_score(map: Grid, trailhead: Location, unique: bool = False) -> int:
    directions = [
        (0, 1),  # Right
        (0, -1),  # Left
        (1, 0),  # Down
        (-1, 0),  # Up
    ]

    visited = set()
    score = 0

    def recurse(loc, prev_height, path) -> int:
        nonlocal score

        # Already visited
        if loc in visited:
            return

        # Out of bounds
        if not in_bounds(loc, map):
            return

        height = map[loc[0]][loc[1]]

        # Must be increasing by 1 each step
        if height - prev_height != 1:
            return

        visited.add(loc)
        path.append(loc)

        # Reached the goal
        if height == 9:
            score += 1
            # Allow traversing different paths
            if unique:
                visited.clear()
            return

        for d in directions:
            dir_loc = (loc[0] + d[0], loc[1] + d[1])
            recurse(dir_loc, height, path[:])

    recurse(trailhead, -1, [])

    return score


def part1():
    map = parse_input("input.txt")
    trailheads = find_trailheads(map)

    total_score = 0
    print(f"Trailheads: {len(trailheads)}")
    for trailhead in trailheads:
        score = trailhead_score(map, trailhead)
        total_score += score

    print(f"Total score: {total_score}")


def part2():
    map = parse_input("input.txt")
    trailheads = find_trailheads(map)

    total_rating = 0
    print(f"Trailheads: {len(trailheads)}")
    for trailhead in trailheads:
        rating = trailhead_score(map, trailhead, unique=True)
        total_rating += rating

    print(f"Total score: {total_rating}")


part1()
part2()
