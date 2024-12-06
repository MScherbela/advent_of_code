# %%
import numpy as np


def parse_input(fname):
    data = []
    with open(fname) as f:
        for l in f:
            data.append(l.strip())

    grid = np.zeros((len(data), len(data[0])), int)
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            grid[i, j] = 1 if c == "#" else 0
            if c in ">^<v":
                start = (i, j)
                direction = ">^<v".index(c)
    return grid, start, direction


def simulate(grid, pos, direction):
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    rows, cols = grid.shape

    visited = set([pos])
    states = set([(pos, direction)])
    is_loop = False
    while True:
        next_row = pos[0] + directions[direction][0]
        next_col = pos[1] + directions[direction][1]

        if next_row < 0 or next_row >= rows or next_col < 0 or next_col >= cols:
            break  # out of bounds
        if grid[next_row, next_col]:
            direction = (direction - 1) % 4  # turn right
        else:
            pos = (next_row, next_col)
            visited.add(pos)

        current_state = (pos, direction)
        if current_state in states:
            is_loop = True
            break
        states.add(current_state)
    return visited, is_loop


grid, start, direction = parse_input("input.txt")
visited_original, _ = simulate(grid, start, direction)
print(f"Part 1: {len(visited_original)}")

visited_original.remove(start)
n_loops = 0
for v in visited_original:
    grid[v[0], v[1]] = 1
    _, is_loop = simulate(grid, start, direction)
    if is_loop:
        n_loops += 1
    grid[v[0], v[1]] = 0
print(f"Part 2: {n_loops}")

# %%
import matplotlib.pyplot as plt

plt.close("all")
grid_with_path = grid.copy()
for v in visited_original:
    grid_with_path[v[0], v[1]] = 2
plt.imshow(grid_with_path, cmap="viridis")
