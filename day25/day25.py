def parse_input(f: str):
    with open(f, "r") as file:
        parts = file.read().split("\n\n")

    locks = []
    keys = []

    for part in parts:
        lines = part.splitlines()
        is_lock = lines[0] == "#####"
        schematic = lines[1:-1]
        rows, cols = len(schematic), len(schematic[0])
        heights = []
        for j in range(cols):
            num_set = 0
            for i in range(rows):
                num_set += 1 if schematic[i][j] == "#" else 0
            heights.append(num_set)

        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)

    return locks, keys


def fits(lock, key):
    for l, k in zip(lock, key):
        if l + k > 5:
            return False
    return True


def part1():
    locks, keys = parse_input("input.txt")

    num_fits = 0
    for lock in locks:
        for key in keys:
            num_fits += 1 if fits(lock, key) else 0
    return num_fits


print(part1())
