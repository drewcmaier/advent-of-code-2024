from copy import deepcopy
from typing import Dict, List, Tuple
from vector2d import Vector2D

type Grid = List[List[str]]


def parse_input(f) -> Grid:
    with open(f, "r") as file:
        lines = file.readlines()

    grid = []
    for line in lines:
        row = [char for char in line.strip()]
        grid.append(row)

    return grid


def find_frequencies(grid: Grid) -> Dict[str, List[Vector2D]]:
    rows, cols = len(grid), len(grid[0])
    frequencies = {}
    for i in range(rows):
        for j in range(cols):
            char = grid[i][j]
            if char == ".":
                continue

            if char not in frequencies:
                frequencies[char] = []

            frequencies[char].append(Vector2D(i, j))

    return frequencies


def all_pairs(points: List[Vector2D]) -> List[Tuple[Vector2D, Vector2D]]:
    pairs = []
    for i in range(len(points)):
        for j in range(i):
            pairs.append([points[i], points[j]])
    return pairs


def find_antinodes(
    points: Tuple[Vector2D, Vector2D], grid: Grid, extent: range
) -> List[Vector2D]:
    diff = points[0] - points[1]

    # Starting from each antenna location, extend outward to add points
    antinodes = []
    for pos in extent:
        pos_point = points[0] + (diff * pos)
        if in_bounds(pos_point, grid):
            antinodes.append(pos_point)
    for neg in extent:
        neg_point = points[1] - (diff * neg)
        if in_bounds(neg_point, grid):
            antinodes.append(neg_point)

    return antinodes


def in_bounds(pos: Vector2D, grid: Grid) -> bool:
    rows, cols = len(grid), len(grid[0])
    return 0 <= pos.x < rows and 0 <= pos.y < cols


def grid_string(grid: Grid):
    s = ""
    for row in grid:
        for col in row:
            s += col
        s += "\n"
    return s


def part1():
    grid = parse_input("input.txt")
    antinode_grid = deepcopy(grid)

    # Get all groups of frequencies, pair them off, then calculate
    # antinodes between them. Use range(1, 2) to only calculate the 1st
    # wave of antinodes
    unique_antinodes = 0
    frequencies = find_frequencies(grid)
    for f in frequencies:
        pairs = all_pairs(frequencies[f])
        for pair in pairs:
            antinodes = find_antinodes(pair, grid, range(1, 2))
            for antinode in antinodes:
                antinode_grid[antinode.x][antinode.y] = "#"

                # Only count unique locations
                if grid[antinode.x][antinode.y] == ".":
                    unique_antinodes += 1

    print(grid_string(antinode_grid))
    print(f"Unique antinodes: {unique_antinodes}")


def part2():
    grid = parse_input("input.txt")
    antinode_grid = deepcopy(grid)

    # Same as Part 1, but modify extent to {0, dim}, where
    # dim is the max of rows or colums. This is the most we
    # would ever need to extrude
    rows, cols = len(grid), len(grid[0])
    dim = max(rows, cols)
    unique_antinodes = 0
    frequencies = find_frequencies(grid)

    for f in frequencies:
        pairs = all_pairs(frequencies[f])
        for pair in pairs:
            antinodes = find_antinodes(pair, grid, range(0, dim))
            for antinode in antinodes:
                # Prevent double-counting
                if antinode_grid[antinode.x][antinode.y] != "#":
                    unique_antinodes += 1
                    antinode_grid[antinode.x][antinode.y] = "#"

    print(grid_string(antinode_grid))
    print(f"Unique antinodes: {unique_antinodes}")
