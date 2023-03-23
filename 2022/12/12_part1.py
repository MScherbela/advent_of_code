import numpy as np
import matplotlib.pyplot as plt

heightmap = []
with open("12/input.txt") as f:
    for line in f:
        line = line.strip()
        row = [ord(c)-ord('a') for c in line]
        heightmap.append(row)

heightmap = np.array(heightmap, int)
pos_start = tuple(np.array(np.where(heightmap == -14))[:,0]) # S
pos_end = tuple(np.array(np.where(heightmap == -28))[:,0])   # E
heightmap[pos_start[0], pos_start[1]] = 0
heightmap[pos_end[0], pos_end[1]] = 25

def get_neighbors(row, col, n_rows, n_cols):
    neighbors = [(row-1, col),
                 (row+1, col),
                 (row, col-1),
                 (row, col+1)]
    neighbors = [n for n in neighbors if (0 <= n[0] < n_rows) and (0 <= n[1] < n_cols)]
    return neighbors

def can_reach(height_start, height_end):
    return height_end <= (height_start + 1)

def get_shortest_path(pos_start, pos_end, heightmap):
    best_next_neighbor = dict()
    distance_to_end = np.ones_like(heightmap) * 1e6
    distance_to_end[pos_end[0], pos_end[1]] = 0
    current_nodes = [pos_end]
    n_steps = 0
    while pos_start not in current_nodes:
        n_steps += 1
        new_nodes = []
        for pos in current_nodes:
            for neighbor in get_neighbors(*pos, *heightmap.shape):
                if can_reach(heightmap[neighbor[0], neighbor[1]], heightmap[pos[0], pos[1]]):
                    if n_steps < distance_to_end[neighbor[0], neighbor[1]]:
                        distance_to_end[neighbor[0], neighbor[1]] = n_steps
                        best_next_neighbor[neighbor] = pos
                        new_nodes.append(neighbor)
        current_nodes = new_nodes
        if len(current_nodes) == 0:
            return 1e6, []

    shortest_path = []
    pos = pos_start
    while pos != pos_end:
        shortest_path.append(pos)
        pos = best_next_neighbor[pos]
    shortest_path.append(pos_end)
    return n_steps, shortest_path

n_steps, path = get_shortest_path(pos_start, pos_end, heightmap)
path = np.array(path)
print(n_steps)
plt.imshow(heightmap)
plt.plot(path[:, 1], path[:, 0], color='r')



# #%%
# possible_starting_points = np.array(np.where(heightmap == 0)).T
# path_lenghts = []
# for i, pos_start in enumerate(possible_starting_points):
#     pos_start = tuple(pos_start)
#     path_lenghts.append(get_shortest_path(pos_start, pos_end, heightmap))
#     print(i, min(path_lenghts))
# print(min(path_lenghts))


