# %%
import numpy as np


def parse_input(fname):
    locks = []
    keys = []
    with open(fname) as f:
        while True:
            current_block = []
            for i in range(8):
                current_block.append(f.readline().strip())
            assert len(current_block[-1]) == 0
            grid = np.array([[c == "#" for c in line] for line in current_block[:-1]])
            if grid.size == 0:
                break
            if grid[0, 0]:
                lock_heights = tuple([int(x - 1) for x in np.sum(grid, axis=0)])
                locks.append(lock_heights)
            else:
                key_heights = tuple([int(x - 1) for x in np.sum(grid, axis=0)])
                keys.append(key_heights)
    return locks, keys


locks, keys = parse_input("input.txt")

n_fit = 0
for lock in locks:
    for key in keys:
        for v1, v2 in zip(lock, key):
            if v1 + v2 > 5:
                break
        else:
            n_fit += 1
print(f"Part 1: {n_fit}")
