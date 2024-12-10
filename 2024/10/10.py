# %%
import numpy as np
import matplotlib.pyplot as plt


def parse_input(fname):
    data = []
    with open(fname) as f:
        for l in f:
            data.append([int(c) for c in l.strip()])
    return np.array(data, dtype=int)


def get_neighbours(r, c, grid):
    val = grid[r, c]
    uphill_val = val + 1
    neigbours = []
    if (r > 0) and (grid[r - 1, c] == uphill_val):
        neigbours.append((r - 1, c))
    if (r < grid.shape[0] - 1) and (grid[r + 1, c] == uphill_val):
        neigbours.append((r + 1, c))
    if (c > 0) and (grid[r, c - 1] == uphill_val):
        neigbours.append((r, c - 1))
    if (c < grid.shape[1] - 1) and (grid[r, c + 1] == uphill_val):
        neigbours.append((r, c + 1))
    return neigbours


grid = parse_input("input.txt")

starting_points = [(int(r), int(c)) for (r, c) in zip(*np.where(grid == 0))]

part1 = 0
for r, c in starting_points:
    frontier = set([(r, c)])
    trail_ends = set()
    while frontier:
        r, c = frontier.pop()
        if grid[r, c] == 9:
            trail_ends.add((r, c))
            continue

        for r_, c_ in get_neighbours(r, c, grid):
            frontier.add((r_, c_))
    part1 += len(trail_ends)
print(f"Part 1: {part1}")


def get_nr_of_distinct_paths(pos, grid, cache):
    if pos in cache:
        return cache[pos]
    val = grid[pos[0], pos[1]]
    neighbours = get_neighbours(*pos, grid)
    if val == 8:
        return len(neighbours)
    else:
        n_paths = 0
        for n in neighbours:
            n_paths += get_nr_of_distinct_paths(n, grid, cache)
    cache[pos] = n_paths
    return n_paths


part2 = 0
cache = {}
for pos in starting_points:
    part2 += get_nr_of_distinct_paths(pos, grid, cache)
print(f"Part2: {part2}")
