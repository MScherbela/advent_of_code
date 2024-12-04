# %%
import numpy as np
import matplotlib.pyplot as plt

fname = "input.txt"


def parse_input(fname):
    with open(fname) as f:
        lines = [l.strip() for l in f]
    n_rows = len(lines)
    n_cols = len(lines[0].strip())
    grid = np.zeros((n_rows, n_cols), dtype=np.int32)
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            grid[i, j] = "#.>^<v".index(c)
    is_path = grid > 0
    n_neighbours = np.zeros((n_rows, n_cols), dtype=np.int32)
    n_neighbours[:-1, :] += is_path[1:, :]
    n_neighbours[1:, :] += is_path[:-1, :]
    n_neighbours[:, :-1] += is_path[:, 1:]
    n_neighbours[:, 1:] += is_path[:, :-1]
    is_node = is_path & (n_neighbours > 2)
    is_node[0, :] = is_path[0, :]
    is_node[-1, :] = is_path[-1, :]
    return grid, is_path, is_node


def get_passable_neighbours(r, c, grid):
    rows, cols = grid.shape
    neighbours = []
    if (r > 0) and ((grid[r - 1, c] == 1) or (grid[r - 1, c] == 3)):
        neighbours.append((r - 1, c))
    if (r < rows - 1) and ((grid[r + 1, c] == 1) or (grid[r + 1, c] == 5)):
        neighbours.append((r + 1, c))
    if (c > 0) and ((grid[r, c - 1] == 1) or (grid[r, c - 1] == 4)):
        neighbours.append((r, c - 1))
    if (c < cols - 1) and ((grid[r, c + 1] == 1) or (grid[r, c + 1] == 2)):
        neighbours.append((r, c + 1))
    return neighbours


def get_edges(starting_node, grid, is_node):
    nodes = set([(int(r), int(c)) for r, c in zip(*np.where(is_node))])
    is_path = grid > 0
    r, c = starting_node
    edges = []
    for starting_pos in get_passable_neighbours(r, c, grid):
        # Start path search
        path = [starting_node, starting_pos]
        pos = starting_pos
        while pos not in nodes:
            # Try all 4 possible ways forward
            passable_neighbours = get_passable_neighbours(*pos, grid)
            passable_neighbours = [n for n in passable_neighbours if n != path[-2]]
            if len(passable_neighbours) == 1:
                path.append(passable_neighbours[0])
                pos = passable_neighbours[0]
            elif len(passable_neighbours) == 0:
                break
            else:
                raise ValueError("Should not happen")
        if pos in nodes:
            edges.append((pos, len(path) - 1))
    return edges


def get_longest_path(start_node, end_node, edges, visited):
    path_lengths = []
    for next_node, length in edges[start_node]:
        if next_node in visited:
            continue
        if next_node == end_node:
            return length
        l = length + get_longest_path(next_node, end_node, edges, visited | {next_node})
        path_lengths.append(l)
    if path_lengths:
        return max(path_lengths)
    return -1_000_000


grid, is_path, is_node = parse_input(fname)

# Part 1
nodes = [(int(r), int(c)) for r, c in zip(*np.where(is_node))]
edges = {src: get_edges(src, grid, is_node) for src in nodes}
start_node, end_node = nodes[0], nodes[-1]
l = get_longest_path(start_node, end_node, edges, {start_node})
print("Part 1:", l)

# Part 2:
grid[grid > 1] = 1
edges = {src: get_edges(src, grid, is_node) for src in nodes}
start_node, end_node = nodes[0], nodes[-1]
l = get_longest_path(start_node, end_node, edges, {start_node})
print("Part 2:", l)
