import numpy as np
import re


def parse_input(f):
    with open(f, "r") as file:
        parts = file.read().split("\n\n")

    machines = []

    button_pattern = re.compile(r"Button [\w]: X([\+\-\d]+), Y([\+\-\d]+)")
    prize_pattern = re.compile(r"Prize: X=([\+\-\d]+), Y=([\+\-\d]+)")

    for part in parts:
        lines = part.splitlines()
        a_match = button_pattern.match(lines[0]).groups()
        a_xy = [int(a) for a in a_match]
        b_match = button_pattern.match(lines[1]).groups()
        b_xy = [int(b) for b in b_match]
        prize_match = prize_pattern.match(lines[2]).groups()
        prize_xy = [int(p) for p in prize_match]

        machines.append((a_xy, b_xy, prize_xy))

    return machines


def part1():
    machines = parse_input("input.txt")

    sum = 0
    for a_xy, b_xy, prize_xy in machines:
        coeff = np.array([[a_xy[0], b_xy[0]], [a_xy[1], b_xy[1]]])
        p = np.array(prize_xy)
        solution = np.linalg.solve(coeff, p)

        is_solution = np.all(np.isclose(np.round(solution), solution))
        if not is_solution:
            continue

        if np.any(np.greater_equal(solution, 100)):
            continue

        token_cost = np.multiply(solution, [3, 1])
        token_sum = np.sum(token_cost)
        sum += token_sum

    return int(sum)


def part2():
    machines = parse_input("input.txt")

    sum = 0
    for a_xy, b_xy, prize_xy in machines:
        coeff = np.array([[a_xy[0], b_xy[0]], [a_xy[1], b_xy[1]]])
        p = np.array(np.add(prize_xy, 10000000000000))

        solution = np.linalg.solve(coeff, p)
        solution_rounded = np.astype(np.round(solution), np.int64)

        is_solution = np.all(np.isclose(solution_rounded, solution, rtol=0, atol=1e-4))
        if not is_solution:
            continue

        token_cost = np.multiply(solution_rounded, [3, 1])
        token_sum = np.sum(token_cost)
        sum += token_sum

    return sum


print(part2())
