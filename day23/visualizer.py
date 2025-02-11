import networkx as nx
import matplotlib.pyplot as plt


with open("input.txt", "r") as file:
    lines = file.readlines()

edges = [line.strip().split("-") for line in lines]

# Create a graph
G = nx.Graph()
G.add_edges_from(edges)

# Draw the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)  # Layout for positioning nodes
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="skyblue",
    edge_color="gray",
    node_size=2000,
    font_size=10,
    font_weight="bold",
)

# Show the plot
plt.title("Graph Visualization")
plt.show()
