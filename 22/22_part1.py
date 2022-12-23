import numpy as np
import matplotlib.pyplot as plt

def parse_input(fname):
    grid = []
    with open(fname) as f:
        for line in f:
            line = line.replace("\n", "")
            if len(line) == 0:
                continue
            if 'R' in line:
                instruction_string = line
                continue
            mapping = {' ': 0, '.': 1, '#': 2}
            grid.append([mapping[c] for c in line])

    width = max([len(r) for r in grid])
    height = len(grid)
    for i in range(height):
        grid[i] = grid[i] + [0] * (width - len(grid[i]))
    grid = np.array(grid, int)

    instructions = []
    number_string = ""
    for c in instruction_string:
        if c.isnumeric():
            number_string += c
        else:
            if number_string:
                instructions.append(("move", int(number_string)))
                number_string = ""
            instructions.append(("rotate", c))
    if number_string:
        instructions.append(("move", int(number_string)))
    return grid, instructions

# grid, instructions = parse_input("22/test_input.txt")
grid, instructions = parse_input("22/input.txt")

row_boundaries = []
for row in grid:
    ind_field = np.where(row != 0)[0]
    row_boundaries.append([ind_field[0], ind_field[-1]])
row_boundaries = np.array(row_boundaries)

col_boundaries = []
for col in grid.T:
    ind_field = np.where(col != 0)[0]
    col_boundaries.append([ind_field[0], ind_field[-1]])
col_boundaries = np.array(col_boundaries)

plt.close("all")
plt.figure()
plt.imshow(grid)

pos = np.array([0, row_boundaries[0, 0]], int)
assert grid[pos[0], pos[1]] == 1
direction = 0 # 0: right, 1: down, 2: left, 3: up
delta = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]], int)

for ins, ins_data in instructions:
    if ins == "rotate":
        if ins_data == "R":
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4
    else:
        for n in range(ins_data):
            col_bound = col_boundaries[pos[1]]
            row_bound = row_boundaries[pos[0]]
            new_pos = pos + delta[direction]
            if new_pos[0] > col_bound[1]:
                new_pos[0] = col_bound[0]
            if new_pos[0] < col_bound[0]:
                new_pos[0] = col_bound[1]
            if new_pos[1] > row_bound[1]:
                new_pos[1] = row_bound[0]
            if new_pos[1] < row_bound[0]:
                new_pos[1] = row_bound[1]
            if grid[new_pos[0], new_pos[1]] == 2:
                break
            else:
                pos = new_pos

pw = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + direction
print(pw)


