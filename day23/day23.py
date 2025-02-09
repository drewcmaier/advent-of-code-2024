class Node:
    def __init__(self, value: str):
        self.value = value
        self.children = set[Node]()

    def __repr__(self):
        return f"{self.value}"


type Graph = dict[str, Node]


def parse_input(f: str):
    with open(f, "r") as file:
        lines = file.readlines()

    return [line.strip().split("-") for line in lines]


def build_graph(adjacencies: list[list[str]]):
    nodes = dict[str, Node]()
    for a1, a2 in adjacencies:
        n1, n2 = nodes.setdefault(a1, Node(a1)), nodes.setdefault(a2, Node(a2))

        n1.children.add(n2)
        n2.children.add(n1)

    return nodes


def get_cycles_of_length(graph: Graph, length: int):
    def recurse(cur: Node, root: Node, path: set[Node], all_paths: set[Node]):
        if len(path) == length:
            if cur == root:
                all_paths.add(frozenset(path))
        else:
            for child in cur.children:
                if child not in path:
                    recurse(child, root, path | {child}, all_paths)

    cycles = set[frozenset]()
    for node in graph.values():
        recurse(node, node, set(), cycles)
    return cycles


def find_chief(cycles: set[frozenset[Node]]):
    has_t = set()
    for cycle in cycles:
        for n in cycle:
            if n.value.startswith("t"):
                has_t.add(cycle)
                break
    return has_t


def cycle_str(cycle: set[Node]):
    return ",".join(sorted([v.value for v in cycle]))


def part1():
    adjacencies = parse_input("test.txt")
    graph = build_graph(adjacencies)
    cycles = get_cycles_of_length(graph, 3)

    s = "\n".join([",".join([v.value for v in c]) for c in cycles])
    print(s)

    has_t = find_chief(cycles)
    print(sorted([cycle_str(c) for c in has_t]))


part1()
