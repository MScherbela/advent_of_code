#%%
import numpy as np
import matplotlib.pyplot as plt

def parse_input(fname):
    data = []
    char_map = {'.': 0, 'O': 1, '#': 2}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            data.append([char_map[c] for c in line])
    return np.array(data, int)

def get_resting_point(data):
    stop_grid = (data == 2)
    rest_map = np.zeros_like(data)
    for col in range(data.shape[1]):
        current_rest = 0
        for row in range(data.shape[0]):
            if stop_grid[row, col]:
                current_rest = row+1
            rest_map[row, col] = current_rest
    return rest_map

def tilt(positions, rest_map, direction):
    nr_of_stones_at_rest = {}
    if direction in ["north", "south"]:
        for (row, col) in positions:
            rest_pos = (rest_map[row, col], col)
            nr_of_stones_at_rest[rest_pos] = nr_of_stones_at_rest.get(rest_pos, 0) + 1
    elif direction in ["west", "east"]:
        for (row, col) in positions:
            rest_pos = (row, rest_map[row, col])
            nr_of_stones_at_rest[rest_pos] = nr_of_stones_at_rest.get(rest_pos, 0) + 1
    new_positions = np.zeros_like(positions)

    ind_pos = 0
    for (row, col), nr in nr_of_stones_at_rest.items():
        if direction == "north":
            new_row = np.arange(row, row+nr)
            new_col = col
        elif direction == "south":
            new_row = np.arange(row, row-nr, -1)
            new_col = col
        elif direction == "west":
            new_row = row
            new_col = np.arange(col, col+nr)
        elif direction == "east":
            new_row = row
            new_col = np.arange(col, col-nr, -1)
        new_positions[ind_pos:ind_pos + nr, 0] = new_row
        new_positions[ind_pos:ind_pos + nr, 1] = new_col
        ind_pos += nr
    return new_positions

def cycle(positions, rest_maps):
    for direction in ["north", "west", "south", "east"]:
        positions = tilt(positions, rest_maps[direction], direction)
    return positions

def calculate_load(positions, n_rows):
    load = n_rows - positions[:, 0]
    return np.sum(load)


data = parse_input("input.txt")
n_rows, n_cols = data.shape
rest_maps = {}

rest_maps["north"] = get_resting_point(data)
rest_maps["south"] = n_rows - 1 - get_resting_point(data[::-1, :])[::-1]
rest_maps["west"] = get_resting_point(data.T).T
rest_maps["east"] = n_cols - 1 - get_resting_point(data[:, ::-1].T).T[:, ::-1]

def hash_positions(positions, n_cols):
    pos_index = positions[:, 0] * n_cols + positions[:, 1]
    pos_index = tuple(sorted(pos_index))
    return hash(pos_index)

positions = np.array(np.where(data == 1)).T

cache = {hash_positions(positions, n_cols): 0}

found_loop = False
n = 0
while not found_loop:
    positions = cycle(positions, rest_maps)
    pos_hash = hash_positions(positions, n_cols)
    if pos_hash in cache:
        n_orig = cache[pos_hash]
        print(f"Found cycle: {n_orig}=={n}")
        cycle_length = n - n_orig
        print(cycle_length)
        n += 1
        break
    else:
        cache[pos_hash] = n
        n += 1

n_iterations = 1_000_000_000
n_leftover = (n_iterations - n) % cycle_length
print(n_leftover)

for _ in range(n_leftover):
    positions = cycle(positions, rest_maps)
load = calculate_load(positions, n_rows)
print("Part 2: ", load)


