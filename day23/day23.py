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
    has_t = 0
    for cycle in cycles:
        for n in cycle:
            if n.value.startswith("t"):
                has_t += 1
                break
    return has_t


def password_str(cycle: set[Node]):
    return ",".join(sorted([v.value for v in cycle]))


def part1(dbg: bool = False):
    adjacencies = parse_input("input.txt")
    graph = build_graph(adjacencies)
    cycles = get_cycles_of_length(graph, 3)

    if dbg:
        print("\n".join(sorted(password_str(c) for c in cycles)))

    return find_chief(cycles)


def bron_kerbosch(
    R: set[Node], P: set[Node], X: set[Node], graph: Graph, cliques: list[set]
):
    if not P and not X:
        cliques.append(R)
        return

    for node in list(P):
        bron_kerbosch(R | {node}, P & node.children, X & node.children, graph, cliques)
        P.remove(node)
        X.add(node)


def find_largest_clique(graph: Graph):
    cliques = []
    bron_kerbosch(set(), set(graph.values()), set(), graph, cliques)
    return max(cliques, key=len) if cliques else set()


def part2():
    adjacencies = parse_input("input.txt")
    graph = build_graph(adjacencies)
    largest_clique = find_largest_clique(graph)
    return password_str(largest_clique)
