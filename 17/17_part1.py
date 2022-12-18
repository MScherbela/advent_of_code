import numpy as np
import matplotlib.pyplot as plt
import dataclasses

with open("17/test_input.txt") as f:
    moves = f.read().strip()

class Block:
    def __init__(self, coords):
        self.coords = coords
        self.width = max([c[1] for c in coords]) + 1
        self.height = max([c[0] for c in coords]) + 1


def can_move_left(x, y, block: Block, grid):
    if x == 0:
        return False
    for dy,dx in block.coords:
        if grid[y + dy, x + dx - 1]:
            return False
    return True

def can_move_right(x, y, block: Block, grid):
    if x + block.width == grid.shape[1]:
        return False
    for dy,dx in block.coords:
        if grid[y + dy, x + dx + 1]:
            return False
    return True

def can_move_down(x, y, block: Block, grid):
    if y == 0:
        return False
    for dy,dx in block.coords:
        if grid[y + dy - 1, x + dx]:
            return False
    return True

def add_to_grid(x, y, block, grid, copy=False, value=1):
    if copy:
        grid = grid.copy()
    for c in block.coords:
        grid[c[0]+y, c[1] + x] = value
    return grid


n_blocks_to_drop = 2022
grid_width = 7
grid_height = n_blocks_to_drop * 4 + 0

BASIC_BLOCKS = [Block([(0, 0), (0, 1), (0, 2), (0, 3)]),
                Block([(2, 1), (1, 0), (1, 1), (1, 2), (0, 1)]),
                Block([(2, 2), (1, 2), (0, 0), (0, 1), (0, 2)]),
                Block([(3, 0), (2, 0), (1, 0), (0, 0)]),
                Block([(1, 0), (1, 1), (0, 0), (0, 1)])]

grid = np.zeros([grid_height, grid_width])
tower_height = 0
ind_input = 0
for ind_block in range(n_blocks_to_drop):
    block = BASIC_BLOCKS[ind_block % len(BASIC_BLOCKS)]
    x = 2
    y = tower_height + 3

    while True:
        m = moves[ind_input % len(moves)]
        ind_input += 1
        if (m == '<') and can_move_left(x, y, block, grid):
            x -= 1
        elif (m == '>') and can_move_right(x, y, block, grid):
            x += 1
        if can_move_down(x, y, block, grid):
            y -= 1
        else:
            grid = add_to_grid(x, y, block, grid)
            tower_height = max(tower_height, y + block.height)
            break

print(tower_height)

# plt.close("all")
# grid = add_to_grid(x, y, block, grid, value=2)
# plt.imshow(grid, origin="lower")
# for x in range(1, grid_width):
#     plt.axvline(x-0.5, color='white', alpha=0.2)
# for y in range(1, grid_height):
#     plt.axhline(y-0.5, color='white', alpha=0.2)




