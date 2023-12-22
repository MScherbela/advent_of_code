#%%
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit, polyval

def parse_input(fname):
    with open(fname) as f:
        grid = [l.strip() for l in f.readlines()]

    for i, row in enumerate(grid):
        if 'S' in row:
            node_start = (i, row.index('S'))
            break
    grid[i] = grid[i].replace('S', '.')

    n_rows, n_cols = len(grid), len(grid[0]) 
    nodes = []
    neighbors = {}
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == '.':
                nodes.append((r, c))
                neighbors[(r, c)] = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    r_n, c_n = (r + dr) % n_rows, (c + dc) % n_cols
                    if grid[r_n][c_n] == '.':
                        neighbors[(r, c)].append((r + dr, c + dc))
    grid = np.array([[1 if c == '.' else 0 for c in row] for row in grid], int)
    return grid, nodes, neighbors, node_start

def get_neighbors(node, neighbor_map, n_rows, n_cols):
    n_cells_row, r = divmod(node[0], n_rows)
    n_cells_col, c = divmod(node[1], n_cols)
    neighbors = neighbor_map[(r, c)]
    return [(r + n_cells_row * n_rows, c + n_cells_col * n_cols) for r, c in neighbors]


def make_steps(nodes, neighbor_map, already_visited, n_steps, ind_step_start=0):
    for ind_step in range(ind_step_start, ind_step_start+n_steps):
        new_nodes = set()
        for node in nodes:
            for neighbor in get_neighbors(node, neighbor_map, n_rows, n_cols):
                if neighbor not in already_visited:
                    new_nodes.add(neighbor)
                    already_visited[neighbor] = ind_step + 1
        nodes = new_nodes
        if ind_step % 10 == 0:
            print(f"{ind_step+1:3d} / {n_steps:3d}: {len(nodes):6d}")
    n_nodes_accessible = 0
    remainder = (ind_step_start + n_steps) % 2
    for s in already_visited.values():
        if s % 2 == remainder:
            n_nodes_accessible += 1
    return nodes, n_nodes_accessible

grid, all_nodes, neighbor_map, node_start = parse_input("/home/mscherbela/develop/advent_of_code/2023/21/input.txt")
n_rows, n_cols = grid.shape
assert n_rows == n_cols
block_width = n_rows

n_steps_total = 26501365
period = block_width * 2

nodes = set([node_start])
already_visited = {}
n_periods_final, n_steps_leftover = divmod(n_steps_total, period)
n_periods_final -= 2
n_steps_leftover += 2*period

n_steps_simulation = n_steps_leftover + 2 * period

print("Running initial leftover steps...")
nodes, n_nodes_accessible = make_steps(nodes, neighbor_map, already_visited, n_steps_leftover)
print(n_nodes_accessible)

n_period_values = np.arange(4)
n_nodes = [n_nodes_accessible]
ind_step = n_steps_leftover
for _ in n_period_values[1:]:
    print(f"Step {ind_step} / {n_steps_simulation}")
    nodes, n_nodes_accessible = make_steps(nodes, neighbor_map, already_visited, period, ind_step)
    n_nodes.append(n_nodes_accessible)
    ind_step += period

coeffs, (residuals, _, _, _)  = polyfit(n_period_values, n_nodes, 2, full=True)
assert residuals < 1e-10
coeffs = [int(np.round(c)) for c in coeffs]
n_nodes_final = n_periods_final**2 * coeffs[2] + n_periods_final * coeffs[1] + coeffs[0]
print(n_nodes_final)


