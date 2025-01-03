# %%
import networkx as nx


def parse_input(fname):
    connections = []
    with open(fname) as f:
        for l in f:
            connections.append(l.strip().split("-"))
    return connections


def build_graph(connections):
    graph = {}
    for c in connections:
        if c[0] not in graph:
            graph[c[0]] = set()
        graph[c[0]].add(c[1])
        if c[1] not in graph:
            graph[c[1]] = set()
        graph[c[1]].add(c[0])
    return graph


def expand_clique(clique, graph):
    new_cliques = set()
    mutual_connections = set.intersection(*[graph[node] for node in clique])
    for m in mutual_connections:
        new_clique = sorted(clique + (m,))
        new_cliques.add(tuple(new_clique))
    return new_cliques


connections = parse_input("input.txt")
graph = build_graph(connections)

cliques = [set([(node,) for node in graph.keys()])]
while cliques[-1]:
    cliques.append(set())
    for c in cliques[-2]:
        cliques[-1].update(expand_clique(c, graph))
cliques = cliques[:-1]

triplets = cliques[2]
largest_clique = cliques[-1].pop()

part1 = len([t for t in triplets if any([x.startswith("t") for x in t])])
part2 = ",".join(sorted(largest_clique))

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
