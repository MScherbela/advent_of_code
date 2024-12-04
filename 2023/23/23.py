# %%
import numpy as np
import matplotlib.pyplot as plt

fname = "test_input.txt"
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

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(grid)
axes[1].imshow(is_node)

nodes = [(int(r), int(c)) for r, c in zip(*np.where(is_node))]


def get_edges(starting_node, grid, is_node):
    r, c = starting_node
    edges = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        visited = np.zeros_like(grid)
        if is_node[r + dr, c + dc]:
            edges.append((r + dr, c + dc))
    return edges
