import numpy as np

coords = []
with open("18/input.txt") as f:
    for line in f:
        tokens = line.strip().split(",")
        coords.append([int(x) for x in tokens])

coords = np.array(coords, int)
extent = coords.max(axis=0) + 2
grid = np.zeros(extent, int)
for c in coords:
    grid[c[0], c[1], c[2]] = 1

area = 0
for x,y,z in coords:
    if grid[x + 1, y, z] == 0:
        area += 1
    if grid[x - 1, y, z] == 0:
        area += 1
    if grid[x, y + 1, z] == 0:
        area += 1
    if grid[x, y - 1, z] == 0:
        area += 1
    if grid[x, y, z + 1] == 0:
        area += 1
    if grid[x, y, z - 1] == 0:
        area += 1
print(area)
