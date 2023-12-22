#%%
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
                    if 0 <= r + dr < n_rows and 0 <= c + dc < n_cols:
                        if grid[r + dr][c + dc] == '.':
                            neighbors[(r, c)].append((r + dr, c + dc))
    return nodes, neighbors, node_start

all_nodes, neighbors, node_start = parse_input("/home/mscherbela/develop/advent_of_code/2023/21/input.txt")
nodes = set([node_start])
n_steps = 64

for ind_step in range(n_steps):
    new_nodes = set()
    for node in nodes:
        for neighbor in neighbors[node]:
            new_nodes.add(neighbor)
    nodes = new_nodes
    print(f"{ind_step+1:3d} / {n_steps:3d}: {len(nodes):5d}")
print(len(nodes))


