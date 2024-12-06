# %%
import numpy as np


def parse_input(fname):
    data = []
    with open(fname) as f:
        for l in f:
            data.append(l.strip())

    n_rows, n_cols = len(data), len(data[0])

    obstacles_per_row = [[] for _ in range(n_rows)]
    obstacles_per_col = [[] for _ in range(n_cols)]
    grid = np.zeros((n_rows, n_cols), dtype=int)
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == "#":
                obstacles_per_row[i].append(j)
                obstacles_per_col[j].append(i)
                grid[i, j] = 1

            if c in ">^<v":
                start = (i, j)
                direction = ">^<v".index(c)
    return grid, obstacles_per_row, obstacles_per_col, start, direction


def step(obstacles_per_row, obstacles_per_col, pos, direction, n_rows, n_cols):
    out_of_bounds = False
    if direction in [0, 2]:
        idx = np.searchsorted(obstacles_per_row[pos[0]], pos[1])
        if (direction == 0) and (idx == len(obstacles_per_row[pos[0]])):
            new_pos = pos[0], n_cols - 1
            out_of_bounds = True
        elif (direction == 2) and (idx == 0):
            new_pos = pos[0], 0
            out_of_bounds = True
        else:
            if direction == 0:
                new_pos = pos[0], obstacles_per_row[pos[0]][idx] - 1
            else:
                new_pos = pos[0], obstacles_per_row[pos[0]][idx - 1] + 1
    else:
        idx = np.searchsorted(obstacles_per_col[pos[1]], pos[0])
        if (direction == 3) and (idx == len(obstacles_per_col[pos[1]])):
            new_pos = n_rows - 1, pos[1]
            out_of_bounds = True
        elif (direction == 1) and (idx == 0):
            new_pos = 0, pos[1]
            out_of_bounds = True
        else:
            if direction == 3:
                new_pos = obstacles_per_col[pos[1]][idx] - 1, pos[1]
            else:
                new_pos = obstacles_per_col[pos[1]][idx - 1] + 1, pos[1]
    direction = (direction - 1) % 4
    return new_pos, direction, out_of_bounds


def is_cycle(obstacles_per_row, obstacles_per_col, pos, direction, n_rows, n_cols):
    visited = set()
    out_of_bounds = False
    while not out_of_bounds:
        pos, direction, out_of_bounds = step(
            obstacles_per_row, obstacles_per_col, pos, direction, n_rows, n_cols
        )
        if (pos, direction) in visited:
            return True
        visited.add((pos, direction))
    return False


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


grid, obs_rows, obs_cols, start, direction = parse_input("input.txt")
visited_original, _ = simulate(grid, start, direction)
print(f"Part 1: {len(visited_original)}")

is_cycle(obs_rows, obs_cols, start, direction, grid.shape[0], grid.shape[1])

visited_original.remove(start)
n_loops = 0
for i, j in visited_original:
    obs_orig = obs_rows[i], obs_cols[j]
    obs_rows[i] = sorted(obs_rows[i] + [j])
    obs_cols[j] = sorted(obs_cols[j] + [i])

    if (i, j) == (4, 6):
        pass
    n_loops += is_cycle(
        obs_rows, obs_cols, start, direction, grid.shape[0], grid.shape[1]
    )
    obs_rows[i], obs_cols[j] = obs_orig

print(f"Part 2: {n_loops}")

# %%
import matplotlib.pyplot as plt

plt.close("all")
grid_with_path = grid.copy()
for v in visited_original:
    grid_with_path[v[0], v[1]] = 2
plt.imshow(grid_with_path, cmap="viridis")
