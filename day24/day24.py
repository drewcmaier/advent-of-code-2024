from collections import deque
import re


def parse_input(f: str):
    with open(f, "r") as file:
        parts = file.read().split("\n\n")

    signal_lines, gate_lines = parts

    signals: dict[str, int] = {}
    signal_pattern = re.compile(r"(\w+): (\d)")
    for signal_line in signal_lines.splitlines():
        signal_id, signal_val = signal_pattern.match(signal_line).groups()
        signals[signal_id] = int(signal_val)

    gates: list[tuple[int, int, str, str, int]] = []
    gate_pattern = re.compile(r"(\w+) (AND|XOR|OR) (\w+) -> (\w+)")
    for gate_line in gate_lines.splitlines():
        signal1, op, signal2, output = gate_pattern.match(gate_line).groups()
        gates.append((signal1, signal2, op, output))

    return signals, gates


def part1():
    signals, gates = parse_input("test2.txt")
    z_values: dict[str, int] = {}

    # Process as a queue, waiting for inputs to exist before processing
    q = deque(gates[:])
    while q:
        gate = q.popleft()
        id1, id2, op, output_id = gate

        if id1 not in signals or id2 not in signals:
            q.append(gate)
            continue

        s1, s2 = signals[id1], signals[id2]
        match op:
            case "AND":
                output = s1 & s2
            case "OR":
                output = s1 | s2
            case "XOR":
                output = s1 ^ s2

        signals[output_id] = output

        if output_id.startswith("z"):
            z_values[output_id] = output

    # for k in sorted(signals.keys()):
    #     print(f"{k}: {signals[k]}")

    z_total = 0
    for i, key in enumerate(sorted(z_values.keys())):
        z_total += z_values[key] << i
    return z_total


print(part1())
