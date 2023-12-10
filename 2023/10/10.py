#%%
import numpy as np
import matplotlib.pyplot as plt

# fname = "test_input.txt"
# start_pipe = "F"
# start_dir = "up"

fname = "input.txt"
start_pipe = "-"
start_dir = "right"

def floodfill(can_fill, start_pos):
    is_filled = np.zeros_like(can_fill)
    frontier = [start_pos]
    while frontier:
        start_pos = frontier.pop()
        for direction in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_pos = (start_pos[0]+direction[0], start_pos[1]+direction[1])
            if new_pos[0] <0 or new_pos[1] < 0 or new_pos[0] >= is_filled.shape[0] or new_pos[1] >= is_filled.shape[1]:
                continue
            if can_fill[new_pos[0]][new_pos[1]] and not is_filled[new_pos[0]][new_pos[1]]:
                frontier.append(new_pos)
                is_filled[new_pos] = True
    return is_filled

with open(fname) as f:
    grid = [l.strip() for l in f.readlines()]

for r, row in enumerate(grid):
    if "S" in row:
        start_row = r
        start_col = row.index("S")
        break
grid[start_row] = grid[start_row].replace("S", start_pipe)

allowed_moves = {
    ("-", "left") : "left",
    ("-", "right") : "right",
    ("|", "up") : "up",
    ("|", "down") : "down",
    ("F", "up"): "right",
    ("F", "left"): "down",
    ("J", "down"): "left",
    ("J", "right"): "up",
    ("7", "up"): "left",
    ("7", "right"): "down",
    ("L", "down"): "right",
    ("L", "left"): "up"
    }

is_loop_ext = np.zeros([2*len(grid), 2*len(grid[0])], dtype=bool)
row, col, direction = start_row, start_col, start_dir
step_counter = 0

while True:
    direction = allowed_moves[(grid[row][col], direction)]
    # print(f"Step {step_counter}: {direction}")
    if direction == "up":
        is_loop_ext[2*row-1, 2*col] = True
        row -= 1
    elif direction == "down":
        is_loop_ext[2*row+1, 2*col] = True
        row += 1
    elif direction == "left":
        is_loop_ext[2*row, 2*col-1] = True
        col -= 1
    elif direction == "right":
        is_loop_ext[2*row, 2*col+1] = True
        col += 1
    is_loop_ext[2*row, 2*col] = True

    step_counter += 1
    if (row, col) == (start_row, start_col):
        break

farthest_distance = step_counter // 2
print(f"Part 1: {farthest_distance}")

is_on_original_grid = np.zeros_like(is_loop_ext)
is_on_original_grid[::2, :][:, ::2] = True
is_inside_extended = ~floodfill(~is_loop_ext, (0, 0))
print(f"Part 2: {np.sum(is_inside_extended & is_on_original_grid & ~is_loop_ext)}")





