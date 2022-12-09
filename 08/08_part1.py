import numpy as np
import matplotlib.pyplot as plt

data = []
with open("08/input.txt") as f:
    for line in f:
        data.append([int(c) for c in line.strip()])
data = np.array(data, int)
is_visible = np.zeros_like(data)
n_rows, n_cols = data.shape

# from the left (downwards), from the right (downwards), from the top (rightwrads), from the bottom (rightwards)
start_points = np.array([(0, 0), (0, n_cols-1), (0, 0), (n_rows-1, 0)], int)
offsets = np.array([(1, 0), (1, 0), (0, 1), (0, 1)], int)
movements = np.array([(0, 1), (0, -1), (1, 0), (-1, 0)])
n_offsets = [n_rows, n_rows, n_cols, n_cols]
n_movements = [n_cols, n_cols, n_rows, n_rows]
n_lines = [n_cols]

for start_index, offset, movement, n_offset, n_move in zip(start_points, offsets, movements, n_offsets, n_movements):
    for i in range(n_offset):
        index = start_index + i * offset
        current_height = -1
        for j in range(n_move):
            if data[index[0], index[1]] > current_height:
                is_visible[index[0], index[1]] = 1
                current_height = data[index[0], index[1]]
            index += movement

print(np.sum(is_visible))
plt.close("all")
plt.imshow(is_visible)

