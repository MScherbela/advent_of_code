import numpy as np
import matplotlib.pyplot as plt

positions = []

with open("23/input.txt") as f:
    for row, line in enumerate(f):
        for col, c in enumerate(line.strip()):
            if c == '#':
                positions.append((row, col))
positions = np.array(positions, int)
padding = 50
positions += padding


def to_grid(positions, padding):
    grid = np.zeros(np.max(positions, axis=0) + padding)
    for p in positions:
        grid[p[0], p[1]] = 1
    return grid


def get_neighboring_values(pos, grid):
    deltas = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    return [grid[pos[0] + r, pos[1] + c] for r, c in deltas]


def get_possible_movements(pos, grid):
    values = get_neighboring_values(pos, grid)
    can_move = [[not (values[-1] or values[0] or values[1]), (-1, 0)],
                [not any(values[3:6]), (1, 0)],
                [not any(values[5:8]), (0, -1)],
                [not any(values[1:4]), (0, 1)]]
    return can_move

def rotate_list(x, n):
    return x[n:] + x[:n]

def add_proposal(proposal_dict, src, tgt):
    src = tuple(src)
    tgt = tuple(tgt)
    if tgt not in proposal_dict:
        proposal_dict[tgt] = []
    proposal_dict[tgt].append(src)
    return proposal_dict

n_iterations = 1000
for n in range(n_iterations):
    if (n % 100) == 0:
        print(f"Iteration {n}")
    grid = to_grid(positions, padding)
    proposals = {}
    n_ = False
    for pos in positions:
        if np.sum(grid[pos[0]-1:pos[0]+2, pos[1]-1:pos[1]+2]) == 1:
            proposals = add_proposal(proposals, pos, pos)
        else:
            possible_movements = get_possible_movements(pos, grid)
            possible_movements = rotate_list(possible_movements, n % 4)
            has_moved = False
            for can_move, delta in possible_movements:
                if can_move:
                    proposals = add_proposal(proposals, pos, (pos[0] + delta[0], pos[1] + delta[1]))
                    has_moved = True
                    any_movement = True
                    break
            if not has_moved:
                proposals = add_proposal(proposals, pos, pos)
    if not any_movement:
        break

    positions = []
    for tgt, srcs in proposals.items():
        if len(srcs) == 1:
            positions.append(tgt)
        else:
            positions += srcs

positions = np.array(positions)
rect_shape = 1 + np.max(positions, axis=0) - np.min(positions, axis=0)
print(np.prod(rect_shape) - len(positions))
print(n+1)

grid = to_grid(positions, padding)
plt.close("all")
plt.imshow(grid)
