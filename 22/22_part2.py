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


grid, instructions = parse_input("22/input.txt")
# grid, instructions = parse_input("22/input.txt")

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

cube_width = min(np.min(row_boundaries[:, 1] - row_boundaries[:, 0]),
                 np.min(col_boundaries[:, 1] - col_boundaries[:, 0])) + 1
cube_side = np.zeros_like(grid)
ind_side = 1
for row in range(cube_side.shape[0] // cube_width):
    for col in range(cube_side.shape[1] // cube_width):
        if grid[row * cube_width, col * cube_width] != 0:
            cube_side[row * cube_width:(row + 1) * cube_width, col * cube_width:(col + 1) * cube_width] = ind_side
            ind_side += 1

cube_side_positions = {}
for i in range(1, 7):
    ind = np.where(cube_side == i)
    cube_side_positions[i] = (ind[0].min(), ind[1].min())


def get_position_on_side(direction, offset_left, cube_width):
    if direction == 0:
        return np.array([offset_left, 0], int)
    if direction == 1:
        return np.array([0, cube_width - offset_left - 1])
    if direction == 2:
        return np.array([cube_width - offset_left - 1, cube_width - 1])
    if direction == 3:
        return np.array([cube_width - 1, offset_left])

def get_offset_left(direction, row, col, cube_width):
    if direction == 0:
        return row
    if direction == 1:
        return cube_width - 1 - col
    if direction == 2:
        return cube_width - 1 - row
    if direction == 3:
        return col

def get_boundaries_test_input():
    boundaries = {(1, 0): (6, 2),
                  (1, 2): (3, 1),
                  (1, 3): (2, 1),
                  (2, 3): (1, 1),
                  (2, 1): (5, 3),
                  (2, 2): (6, 3),
                  (3, 1): (5, 0),
                  (3, 3): (1, 0),
                  (4, 0): (6, 1),
                  (5, 1): (2, 3),
                  (5, 2): (3, 3),
                  (6, 0): (1, 2),
                  (6, 1): (2, 0),
                  (6, 3): (4, 2)}
    for src, tgt in boundaries.items():
        rev_src = (tgt[0], (tgt[1] + 2) % 4)
        rev_tgt = (src[0], (src[1] + 2) % 4)
        assert boundaries[rev_src] == rev_tgt
    return boundaries


def get_boundaries_input():
    boundaries = {(1, 2): (4, 0),
                  (1, 3): (6, 0),
                  (2, 0): (5, 2),
                  (2, 1): (3, 2),
                  (2, 3): (6, 3),
                  (3, 0): (2, 3),
                  (3, 2): (4, 1),
                  (4, 2): (1, 0),
                  (4, 3): (3, 0),
                  (5, 0): (2, 2),
                  (5, 1): (6, 2),
                  (6, 0): (5, 3),
                  (6, 1): (2, 1),
                  (6, 2): (1, 1)}
    for src, tgt in boundaries.items():
        rev_src = (tgt[0], (tgt[1] + 2) % 4)
        rev_tgt = (src[0], (src[1] + 2) % 4)
        assert boundaries[rev_src] == rev_tgt
    return boundaries

pos = np.array([0, row_boundaries[0, 0]], int)
current_side = cube_side[pos[0], pos[1]]
direction = 0  # 0: right, 1: down, 2: left, 3: up
delta = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]], int)
boundaries = get_boundaries_input()
assert grid[pos[0], pos[1]] == 1
#
# pos = np.array([1, 11], int)
# direction = 0
# instructions = [('move', 1)]

path = [pos]
for ins, ins_data in instructions:
    if ins == "rotate":
        if ins_data == "R":
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4
    else:
        for n in range(ins_data):
            new_pos = pos + delta[direction]
            new_direction = direction
            new_side = cube_side[new_pos[0] % grid.shape[0], new_pos[1] % grid.shape[1]]
            if new_side != current_side:
                # leaving a cube side
                if (current_side, direction) in boundaries:
                    # non-trivial boundary
                    new_side, new_direction = boundaries[(current_side, direction)]
                    corner = cube_side_positions[current_side]
                    new_corner = cube_side_positions[new_side]
                    offset = get_offset_left(direction, *(pos - corner), cube_width)
                    new_pos = get_position_on_side(new_direction, offset, cube_width) + new_corner
            if grid[new_pos[0], new_pos[1]] == 2:
                break
            else:
                pos = new_pos
                direction = new_direction
                current_side = new_side
                path.append(pos)

path = np.array(path)

plt.close("all")
plt.figure()
plt.imshow(grid)
plt.plot(path[:, 1], path[:, 0], ls='None', marker='o', color='r')


pw = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + direction
print(pw)

