#%%
import numpy as np

def parse_input(fname):
    data = []
    char_map = {'.': 0, 'O': 1, '#': 2}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            data.append([char_map[c] for c in line])
    return np.array(data, int)

def tilt_north(data):
    n_rows, n_cols = data.shape
    for n_steps in range(n_rows):
        for row in range(1, n_rows):
            for col in range(n_cols):
                if (data[row, col] == 1) and (data[row - 1, col] == 0):
                    data[row - 1, col] = 1
                    data[row, col] = 0
    return data

def get_total_load(data):
    load = 0
    n_rows = data.shape[0]
    for ind_row, row in enumerate(data):
        load_factor = n_rows - ind_row
        load += load_factor * sum(row == 1)
    return load


data = parse_input("input.txt")
data = tilt_north(data)
total_load_part1 = get_total_load(data)

print("Part 1: ", total_load_part1)