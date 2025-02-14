import graphviz
from collections import defaultdict
from day24 import parse_input, evaluate_graph

signals, gates = parse_input("input.txt")
signals = dict(sorted(signals.items()))

graph = {}
for var1, var2, op, output in gates:
    graph[output] = (var1, var2, op)

swaps = [("z18", "fvw"), ("z36", "nwq"), ("z22", "mdb"), ("wpq", "grf")]
for a, b in swaps:
    graph[a], graph[b] = graph[b], graph[a]

graph = dict(sorted(graph.items()))

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

result = evaluate_graph(graph, test_signals)

dependencies = defaultdict(set)
reverse_dependencies = defaultdict(set)

for output, (a, b, _) in graph.items():
    dependencies[a].add(output)
    dependencies[b].add(output)
    reverse_dependencies[output].update([a, b])

for n in graph:
    a, b, op = graph[n]
    if n.startswith("z"):
        if op != "XOR":
            print(f"mismatched output: {n}")
    if (
        a.startswith("x")
        and not b.startswith("y")
        or a.startswith("y")
        and not b.startswith("x")
    ):
        print(n)


dot = graphviz.Digraph("RippleCarryAdder", format="png")
dot.attr(rankdir="LR", ordering="in", splines="false")

for n in dependencies:
    dot.node(n, f"{n}: {result[n]}", shape="circle")

for output, (a, b, op) in graph.items():
    op_id = f"{output}_{op}"
    match op:
        case "AND":
            shape = "triangle"
            color = "chartreuse4"
        case "OR":
            shape = "invtriangle"
            color = "darkblue"
        case "XOR":
            shape = "doublecircle"
            color = "coral1"
    dot.node(op_id, op, shape=shape, color=color)
    dot.edge(a, op_id)
    dot.edge(b, op_id)
    dot.edge(op_id, output, f"{result[output]}")

dot.render("circuit", view=True)
