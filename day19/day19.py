from functools import cache


def parse_input(f) -> tuple[set[str], list[str]]:
    with open(f, "r") as file:
        parts = file.read().split("\n\n")

    patterns = parts[0].split(", ")
    designs = parts[1].split("\n")

    return (set(patterns), designs)


def is_valid_design(design: str, patterns: set[str]):
    @cache
    def recurse(design):
        if design == "":
            return True

        for pattern in patterns:
            if design.startswith(pattern):
                if recurse(design[len(pattern) :]):
                    return True

        return False

    return recurse(design)


def part1():
    patterns, designs = parse_input("input.txt")

    total_valid = 0
    for design in designs:
        if is_valid_design(design, patterns):
            total_valid += 1
    return total_valid


def num_valid_combinations(design: str, patterns: set[str]) -> int:
    @cache
    def recurse(design):
        if design == "":
            return 1

        combinations = 0
        for pattern in patterns:
            if design.startswith(pattern):
                combinations += recurse(design[len(pattern) :])

        return combinations

    return recurse(design)


def part2():
    patterns, designs = parse_input("input.txt")

    total_combos = 0
    for design in designs:
        combos = num_valid_combinations(design, patterns)
        total_combos += combos

    return total_combos
