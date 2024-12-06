# %%
import numpy as np


def parse_input(fname):
    constraints = set()
    data = []
    with open(fname) as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            if "|" in l:
                x, y = map(int, l.split("|"))
                constraints.add((x, y))
            else:
                data.append(list(map(int, l.split(","))))
    return data, constraints


def build_edges(nodes, constraints):
    node_set = set(nodes)
    edges = {n: [] for n in nodes}
    for dependency, node in constraints:
        if (node not in node_set) or (dependency not in node_set):
            continue
        edges[node].append(dependency)
    return edges


def dfs(node, edges, visited=None, current_parents=None):
    visited = visited or set()
    current_parents = current_parents or set()
    visited.add(node)
    current_parents.add(node)
    visit_order = []
    for n in edges[node]:
        if n in current_parents:
            raise ValueError("Cycle detected")
        if n in visited:
            continue
        visit_order += dfs(n, edges, visited, current_parents)
    current_parents.remove(node)
    visit_order.append(node)
    return visit_order


def topological_sort(nodes, edges):
    unsorted_nodes = set(nodes)
    visited = set()
    sorted_output = []
    while unsorted_nodes:
        starting_node = next(iter(unsorted_nodes))
        visit_order = dfs(starting_node, edges, visited)
        for n in visit_order:  # starting node has already been popped
            unsorted_nodes.remove(n)
            visited.add(n)
        sorted_output += visit_order
    return sorted_output


data, constraints = parse_input("input.txt")

# Part 1
sum_part1 = 0
sum_part2 = 0
for idx_d, d in enumerate(data):
    is_valid = True
    for i, x1 in enumerate(d):
        for j in range(i + 1, len(d)):
            x2 = d[j]
            if (x2, x1) in constraints:
                is_valid = False
                break
        if not is_valid:
            break
    if is_valid:
        sum_part1 += d[len(d) // 2]
    else:
        edges = build_edges(d, constraints)
        sorted_nodes = topological_sort(d, edges)
        sum_part2 += sorted_nodes[len(sorted_nodes) // 2]
print(f"Part 1: {sum_part1}")
print(f"Part 2: {sum_part2}")
