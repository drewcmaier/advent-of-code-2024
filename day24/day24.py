import re
from copy import deepcopy
from itertools import combinations, permutations

type Graph = dict[str, tuple[str, str, str]]


def parse_input(f: str):
    with open(f, "r") as file:
        parts = file.read().split("\n\n")

    signal_lines, gate_lines = parts

    signals: dict[str, int] = {}
    signal_pattern = re.compile(r"(\w+): (\d)")
    for signal_line in signal_lines.splitlines():
        signal_id, signal_val = signal_pattern.match(signal_line).groups()
        signals[signal_id] = int(signal_val)

    gates: list[tuple[str, str, str, str]] = []
    gate_pattern = re.compile(r"(\w+) (AND|XOR|OR) (\w+) -> (\w+)")
    for gate_line in gate_lines.splitlines():
        signal1, op, signal2, output = gate_pattern.match(gate_line).groups()
        sorted_signals = sorted([signal1, signal2])
        gates.append((sorted_signals[0], sorted_signals[1], op, output))

    return signals, gates


def bin_val(d: dict[str, int]):
    return sum(d[key] << i for i, key in enumerate(sorted(d.keys())))


def apply_operation(val1: int, val2: int, op: str):
    if val1 is None or val2 is None:
        return None

    if op == "AND":
        return val1 & val2
    elif op == "OR":
        return val1 | val2
    elif op == "XOR":
        return val1 ^ val2


def evaluate_graph(graph: Graph, inputs: dict[str, int]):
    values = inputs.copy()
    visited = set()

    def compute(var):
        if var in values:
            return values[var]

        if var in visited:
            return None

        visited.add(var)

        if var in graph:
            var1, var2, op = graph[var]
            values[var] = apply_operation(compute(var1), compute(var2), op)

        return values[var]

    for output in graph:
        compute(output)

    return values


def part1():
    signals, gates = parse_input("input.txt")

    graph: Graph = {}
    for var1, var2, op, output in gates:
        graph[output] = (var1, var2, op)

    result = evaluate_graph(graph, signals)

    z = {}
    for k in sorted(result.keys()):
        if k.startswith("z"):
            z[k] = result[k]

    return bin_val(z)


def run_graph(graph, signals, dbg=False):
    result = evaluate_graph(graph, signals)

    if None in result.values():
        return None

    x, y, z = [], [], []
    for k in sorted(result.keys()):
        if k.startswith("x"):
            x.append(result[k])
        elif k.startswith("y"):
            y.append(result[k])
        elif k.startswith("z"):
            z.append(result[k])

    s = ""
    x.append(0)
    y.append(0)

    s += "\nx\n"
    x_str = "0"
    for k in x:
        s += f"{str(k)}"
        x_str += str(k)

    s += "\ny\n"
    y_str = "0"
    for k in y:
        s += f"{str(k)}"
        y_str += str(k)

    s += "\nz\n"
    z_str = ""
    for k in z:
        s += f"{str(k)}"
        z_str += str(k)

    wrong_bits = []
    carry = 0
    for i in range(len(x)):
        ripple_sum = x[i] ^ y[i] ^ carry
        carry = (x[i] & y[i]) | (carry & (x[i] ^ y[i]))
        if ripple_sum != z[i]:
            wrong_bits.append(i)

    def list_bin_val(l):
        return int("0b" + "".join([str(li) for li in reversed(l)]), 2)

    x_val, y_val, z_val = list_bin_val(x), list_bin_val(y), list_bin_val(z)
    if dbg:
        print(s)
        print(f"Wrong bits: {wrong_bits}")
        print(f"{x_val} + {y_val} =\nexpected:\t{x_val + y_val}\nactual:\t\t{z_val}")
    return z_val


def part2(dbg=False):
    signals, gates = parse_input("test3.txt" if dbg else "input.txt")

    graph: Graph = {}
    for var1, var2, op, output in gates:
        graph[output] = (var1, var2, op)

    swaps = [("z18", "fvw"), ("z36", "nwq"), ("z22", "mdb")]
    for a, b in swaps:
        graph[a], graph[b] = graph[b], graph[a]

    locked_outputs = set()
    for a, b in swaps:
        locked_outputs.update([a, b])

    correct = run_graph(graph, signals, dbg=True)
    print(correct)

    test_signals = signals.copy()

    for i in range(45):
        test_signals[f"x{i:02d}"] = 0
        test_signals[f"y{i:02d}"] = 0

    test_signals["x00"] = 1
    test_signals["x01"] = 1
    test_signals["x02"] = 1
    test_signals["x03"] = 1
    test_signals["x04"] = 1
    test_signals["x05"] = 1
    test_signals["y00"] = 1

    # for i in range(6):
    #     test_signals[f"x{i:02d}"] = 1
    #     print(run_graph(graph, test_signals, dbg=True))
    #     pass

    # Brute force the last one
    for o1, o2 in combinations(graph.keys(), 2):
        if o1 in locked_outputs or o2 in locked_outputs:
            continue

        test_graph = graph.copy()
        test_graph[o1], test_graph[o2] = test_graph[o2], test_graph[o1]

        test_result = run_graph(test_graph, test_signals)
        if test_result == 64:
            print("CORRECT", o1, o2, test_result)


part2(dbg=False)
