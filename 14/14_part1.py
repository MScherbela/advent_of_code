import numpy as np
import matplotlib.pyplot as plt

lines = []
with open("14/input.txt") as f:
    for line in f:
        points = line.strip().split(" -> ")
        lines.append([[int(p.split(",")[0]),int(p.split(",")[1])] for p in points])

all_points = []
for l in lines:
    all_points += l
all_points = np.array(all_points)
x_min, y_min = np.min(all_points, axis=0)
x_max, y_max = np.max(all_points, axis=0)

x_margin = y_max - y_min + 10
y_margin = 10
x_offset = x_min - x_margin
y_offset = y_min - y_margin

add_floor = True

grid = np.zeros([y_max - y_min + 2*y_margin, x_max - x_min + 2*x_margin], int)
for l in lines:
    l = np.array(l)
    for i in range(len(l)-1):
        x_start, y_start = l[i]
        x_end, y_end = l[i + 1]
        if x_start == x_end:
            if y_start > y_end:
                y_end, y_start = y_start, y_end
            grid[(y_start - y_offset):(y_end - y_offset + 1), (x_start - x_offset)] = 1
        elif y_start == y_end:
            if x_start > x_end:
                x_end, x_start = x_start, x_end
            grid[(y_start - y_offset), (x_start - x_offset): (x_end - x_offset + 1)] = 1
        else:
            raise ValueError("Only allow straight lines")

if add_floor:
    grid[y_max+2-y_offset, :] = 1

is_finished = False
n_particles = 0
while not is_finished:
    n_particles += 1
    pos = np.array([0 - y_offset, 500 - x_offset], int)
    if grid[pos[0], pos[1]] != 0:
        break
    while pos[0] < (grid.shape[0] - 1):
        if grid[pos[0] + 1, pos[1]] == 0:
            pos[0] += 1
        elif grid[pos[0] + 1, pos[1] - 1] == 0:
            pos[0] += 1
            pos[1] -= 1
        elif grid[pos[0] + 1, pos[1] + 1] == 0:
            pos += 1
        else:
            grid[pos[0], pos[1]] = 2
            break
    is_finished = (pos[0] == grid.shape[0] - 1)
print(n_particles-1)

plt.close("all")
plt.imshow(grid, origin='upper')
