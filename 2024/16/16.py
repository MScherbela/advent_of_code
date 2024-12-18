# %%
import numpy as np
import heapq
from collections import defaultdict

DIRECTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]
COST_ROTATE = 1000
COST_MOVE = 1


def parse_input(fname):
    grid = []
    start = None
    end = None
    with open(fname) as f:
        for i, l in enumerate(f):
            grid_line = []
            for j, c in enumerate(l.strip()):
                if c in "SE.":
                    grid_line.append(1)
                else:
                    grid_line.append(0)
                if c == "S":
                    start = (i, j)
                elif c == "E":
                    end = (i, j)
            grid.append(grid_line)
    return np.array(grid, int), start, end


def build_graph(grid):
    graph = {}
    for r, c in zip(*np.where(grid == 1)):
        r, c = int(r), int(c)
        for direction in range(4):
            node = (r, c, direction)
            edges = [(COST_ROTATE, (r, c, (direction + 1) % 4)), (COST_ROTATE, (r, c, (direction - 1) % 4))]
            r_next, c_next = r + DIRECTIONS[direction][0], c + DIRECTIONS[direction][1]
            if grid[r_next, c_next]:
                edges.append((COST_MOVE, (r_next, c_next, direction)))
            graph[node] = edges
    return graph


def find_shortest_paths(graph, start):
    distance = defaultdict(lambda: np.inf)
    distance[start] = 0
    predecessors = defaultdict(set)
    frontier = [(0, start)]
    heapq.heapify(frontier)
    while frontier:
        _, node = heapq.heappop(frontier)
        current_distance = distance[node]
        for dist, n in graph[node]:
            new_distance = current_distance + dist
            if new_distance < distance[n]:
                distance[n] = new_distance
                heapq.heappush(frontier, (distance[n], n))
                predecessors[n] = {node}
            elif new_distance == distance[n]:
                predecessors[n].add(node)
    return distance, predecessors


grid, start, end = parse_input("input.txt")
start = (*start, 0)
end_points = [(*end, d) for d in range(4)]
graph = build_graph(grid)

distances, predecessors = find_shortest_paths(graph, start)
end_distances = [distances[e] for e in end_points]
part1 = min(end_distances)
print(f"Part 1: {part1}")

# Trace back to find all shortest pahts
is_on_shortest_path = set()
frontier = set([e for e in end_points if distances[e] == min(end_distances)])
while frontier:
    node = frontier.pop()
    is_on_shortest_path.add(node[:2])
    for p in predecessors[node]:
        frontier.add(p)
part2 = len(is_on_shortest_path)

print(f"Part 2: {part2}")
