import numpy as np

coords = []
with open("18/input.txt") as f:
    for line in f:
        tokens = line.strip().split(",")
        coords.append([int(x) for x in tokens])

coords = np.array(coords, int)
coords = coords + (np.min(coords, axis=0) + 1)
extent = coords.max(axis=0) + 2
grid = np.zeros(extent, int)
for c in coords:
    grid[c[0], c[1], c[2]] = 1


def get_neighbors(x, y, z, shape):
    neighbors = []
    if x > 0:
        neighbors.append([x - 1, y, z])
    if x < shape[0] - 1:
        neighbors.append([x + 1, y, z])
    if y > 0:
        neighbors.append([x, y - 1, z])
    if y < shape[1] - 1:
        neighbors.append([x, y + 1, z])
    if z > 0:
        neighbors.append([x, y, z - 1])
    if z < shape[2] - 1:
        neighbors.append([x, y, z + 1])
    return neighbors


def floodfill(grid, fill_value):
    # 0: not yet considered, 1: rock, -1: air
    coords_to_consider = [[0, 0, 0]]
    while len(coords_to_consider) > 0:
        new_coords_to_consider = []
        for x, y, z in coords_to_consider:
            if grid[x, y, z] == fill_value:
                continue
            for xn, yn, zn in get_neighbors(x, y, z, grid.shape):
                if grid[xn, yn, zn] == 0:
                    new_coords_to_consider.append([xn, yn, zn])
            grid[x, y, z] = fill_value
        coords_to_consider = new_coords_to_consider
    return grid


print("Running floodfill...")
grid = floodfill(grid, -1)

print("Calculating surface")
area = 0
for x, y, z in coords:
    for xn, yn, zn in get_neighbors(x, y, z, grid.shape):
        if grid[xn, yn, zn] == -1:
            area += 1
print(area)
