import numpy as np
import matplotlib.pyplot as plt
import dataclasses

with open("17/input.txt") as f:
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


FINGERPRINT_DEPTH = 50
def get_top_shape(grid, tower_height):
    top = grid[tower_height-FINGERPRINT_DEPTH:tower_height, :].flatten()
    return tuple(top)


n_blocks_to_drop = 100_000
grid_width = 7
grid_height = n_blocks_to_drop * 4 + 100

BASIC_BLOCKS = [Block([(0, 0), (0, 1), (0, 2), (0, 3)]),
                Block([(2, 1), (1, 0), (1, 1), (1, 2), (0, 1)]),
                Block([(2, 2), (1, 2), (0, 0), (0, 1), (0, 2)]),
                Block([(3, 0), (2, 0), (1, 0), (0, 0)]),
                Block([(1, 0), (1, 1), (0, 0), (0, 1)])]

grid = np.zeros([grid_height, grid_width])
cache = {}

tower_height = 0
ind_input = 0
for ind_block in range(n_blocks_to_drop):
    if (ind_block % 100_000) == 0:
        print(f"{ind_block / 1e6: .1f} mio blocks")
    block_id = ind_block % len(BASIC_BLOCKS)
    block = BASIC_BLOCKS[block_id]
    x = 2
    y = tower_height + 3

    state = (block_id, ind_input, get_top_shape(grid, tower_height))
    if tower_height > FINGERPRINT_DEPTH:
        if state in cache:
            print("Cache hit!")
            break
        else:
            cache[state] = (ind_block, tower_height)

    while True:
        m = moves[ind_input]
        ind_input = (ind_input + 1) % len(moves)
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
base_n_blocks, base_height = cache[state]
period = ind_block - base_n_blocks
delta_height = tower_height - base_height

print(f"Increase in tower height: {delta_height}")  # 102 - 49 = 53 height
print(f"Period in blocks        : {period}")     # 63 - 28 = 35 blocks

n_total = 1000000000000
n_repetitions = (n_total - base_n_blocks) // period
n_additional = n_total - n_repetitions * period - base_n_blocks
ind_to_find = base_n_blocks + n_additional
print(f"Additional steps: {n_additional}")

for ind, height in cache.values():
    if ind == ind_to_find:
        additional_height = height - base_height
        break
print(f"Additional height: {additional_height}")
print(f"Total height: {n_repetitions * delta_height + base_height + additional_height}")
# print(f"Ref solution: 1514285714288")
# plt.close("all")
# grid = add_to_grid(x, y, block, grid, value=2)
# plt.imshow(grid, origin="lower")
# for x in range(1, grid_width):
#     plt.axvline(x-0.5, color='white', alpha=0.2)
# for y in range(1, grid_height):
#     plt.axhline(y-0.5, color='white', alpha=0.2)




