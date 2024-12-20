# %%
import numpy as np
from collections import deque, Counter


def parse_input(fname):
    is_path = []
    start, end = None, None
    with open(fname) as f:
        for r, l in enumerate(f):
            l = l.strip()
            is_path.append([c in ".SE" for c in l])
            if "S" in l:
                start = (r, l.index("S"))
            if "E" in l:
                end = (r, l.index("E"))
    return np.array(is_path, bool), start, end


def build_graph(is_path):
    graph = {}
    for r, row in enumerate(is_path):
        for c, is_open in enumerate(row):
            if not is_open:
                continue
            neighbors = []
            if r > 0 and is_path[r - 1, c]:
                neighbors.append((r - 1, c))
            if r < is_path.shape[0] - 1 and is_path[r + 1, c]:
                neighbors.append((r + 1, c))
            if c > 0 and is_path[r, c - 1]:
                neighbors.append((r, c - 1))
            if c < is_path.shape[1] - 1 and is_path[r, c + 1]:
                neighbors.append((r, c + 1))
            graph[(r, c)] = neighbors
    return graph


def get_nodes_within_distance(start, d_max):
    r_start, c_start = start
    for r in range(r_start - d_max, r_start + d_max + 1):
        for c in range(c_start - d_max, c_start + d_max + 1):
            d = abs(r - r_start) + abs(c - c_start)
            if d <= d_max:
                yield (r, c), d


def bfs(graph, start):
    distance = {start: 0}
    frontier = deque([start])
    while frontier:
        node = frontier.popleft()
        d = distance[node]
        for n in graph[node]:
            if n in distance:
                continue
            distance[n] = d + 1
            frontier.append(n)
    return distance


def get_nr_of_cheats(graph, start, end, dist_cheat_max, save_min=100):
    dist_from_start = bfs(graph, start)
    dist_to_end = bfs(graph, end)
    dist_no_cheat = dist_from_start[end]
    nr_of_cheats = 0
    for node in graph:
        for n, d_cheat in get_nodes_within_distance(node, dist_cheat_max):
            if n in graph:
                d = dist_from_start[node] + dist_to_end[n] + d_cheat
                saving = dist_no_cheat - d
                if saving >= save_min:
                    nr_of_cheats += 1
    return nr_of_cheats


is_path, start, end = parse_input("input.txt")
graph = build_graph(is_path)

part1 = get_nr_of_cheats(graph, start, end, 2)
print(f"Part 1: {part1}")
part2 = get_nr_of_cheats(graph, start, end, 20)
print(f"Part 2: {part2}")
