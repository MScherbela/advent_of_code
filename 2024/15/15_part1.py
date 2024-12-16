# %%
import numpy as np
import matplotlib.pyplot as plt


def parse_input(fname):
    grid = []
    moves = ""
    pos = None
    with open(fname) as f:
        for i, l in enumerate(f):
            l = l.strip()
            if "#" in l or "." in l or "O" in l:
                grid_line = []
                for j, c in enumerate(l):
                    grid_line.append({".": 0, "#": 1, "O": 2, "@": 0}[c])
                    if c == "@":
                        pos = (i, j)
                grid.append(grid_line)
            else:
                moves = moves + l
    return np.array(grid), moves, pos


def step(grid, pos, dir):
    pos_next = pos + dir
    v = grid[pos_next[0], pos_next[1]]
    if v == 0:
        # empty
        return pos_next
    elif v == 1:
        # wall
        return pos
    else:
        while grid[pos_next[0], pos_next[1]] == 2:
            pos_next = pos_next + dir
        if grid[pos_next[0], pos_next[1]] == 0:
            # empty space afterwards => can move
            grid[pos_next[0], pos_next[1]] = 2
            pos_next = pos + dir
            grid[pos_next[0], pos_next[1]] = 0
            return pos_next
        return pos


grid, moves, pos = parse_input("input.txt")
moves_to_dir = {"<": np.array([0, -1]), ">": np.array([0, 1]), "^": np.array([-1, 0]), "v": np.array([1, 0])}
for m in moves:
    dir = moves_to_dir[m]
    pos = step(grid, pos, dir)

box_coords = np.where(grid == 2)
part1 = np.sum(100 * box_coords[0] + box_coords[1])
print(f"Part 1: {part1}")
