def parse_input(f):
    with open(f, "r") as file:
        lines = file.readlines()

    equations = []
    for line in lines:
        parts = line.split(":")
        total = int(parts[0])
        nums = [int(num) for num in parts[1].strip().split()]
        equations.append((total, nums))

    return equations


def num_valid(total, nums):
    def recurse(t, n, valid, s):
        if t == total and len(n) == 0:
            print(s)
            return valid + 1

        if len(n) == 0:
            return valid

        cur = n.pop(0)
        return recurse(t + cur, n[:], valid, f"{s}+{cur}") + recurse(
            t * cur, n[:], valid, f"{s}*{cur}"
        )

    return recurse(0, nums[:], 0, f"{total} = ")


def num_valid_with_concat(total, nums):
    def recurse(t, n, valid, s):
        if t == total and len(n) == 0:
            print(s)
            return valid + 1

        if len(n) == 0:
            return valid

        cur = n.pop(0)
        return (
            recurse(t + cur, n[:], valid, f"{s}+{cur}")
            + recurse(t * cur, n[:], valid, f"{s}*{cur}")
            + recurse(int(f"{t}{cur}"), n[:], valid, f"{s}|{cur}")
        )

    return recurse(0, nums[:], 0, f"{total} = ")


def part1():
    equations = parse_input("test.txt")

    results = []
    for total, nums in equations:
        valid = num_valid(total, nums)
        if valid > 0:
            results.append(total)

    sum = 0
    for r in results:
        sum += r
    return sum


def part2():
    equations = parse_input("input.txt")

    results = []
    for total, nums in equations:
        valid = num_valid_with_concat(total, nums)
        if valid > 0:
            results.append(total)

    sum = 0
    for r in results:
        sum += r
    return sum


print(f"Total: {part2()}")
