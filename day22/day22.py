from collections import defaultdict, deque


def parse_input(f: str):
    with open(f, "r") as file:
        lines = file.readlines()

    return [int(line.strip()) for line in lines]


def generate_secret_number(secret: int, iterations: int):
    for _ in range(iterations):
        secret = ((secret << 6) ^ secret) & 0xFFFFFF  # Equivalent to % 16777216
        secret = ((secret >> 5) ^ secret) & 0xFFFFFF
        secret = ((secret << 11) ^ secret) & 0xFFFFFF

    return secret


def part1():
    initial_numbers = parse_input("input.txt")

    total = sum(generate_secret_number(i, 2000) for i in initial_numbers)
    return total


def generate_prices(secret: int, iterations: int):
    ones = []
    for _ in range(iterations + 1):
        ones.append(secret % 10)
        secret = ((secret << 6) ^ secret) & 0xFFFFFF
        secret = ((secret >> 5) ^ secret) & 0xFFFFFF
        secret = ((secret << 11) ^ secret) & 0xFFFFFF

    return ones


def part2():
    initial_numbers = parse_input("input.txt")

    buyer_prices = defaultdict(dict)  # buyer_idx -> {subseq: max_price}
    subseq_to_buyers = defaultdict(set)  # subseq -> set(buyer_idx)

    for buyer_idx, initial_secret in enumerate(initial_numbers):
        last_4_changes = deque(maxlen=4)
        prices = generate_prices(initial_secret, 2000)

        prev_price = prices[0]
        for price_idx in range(1, len(prices)):
            price = prices[price_idx]
            change = price - prev_price
            last_4_changes.append(change)
            if len(last_4_changes) == 4:
                subseq_tuple = tuple(last_4_changes)
                if subseq_tuple not in buyer_prices[buyer_idx]:
                    buyer_prices[buyer_idx][subseq_tuple] = price

                subseq_to_buyers[subseq_tuple].add(buyer_idx)

            prev_price = price

    return max(
        sum(buyer_prices[buyer_idx].get(subseq, 0) for buyer_idx in buyers)
        for subseq, buyers in subseq_to_buyers.items()
    )


print(part2())
