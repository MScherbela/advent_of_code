#%%
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
import heapq
State = namedtuple("State", ["r", "c", "vr", "vc", "age"])


def parse_input(fname):
    with open(fname) as f:
        lines = [l.strip() for l in f.readlines()]
        data = [[int(c) for c in line] for line in lines]
        return np.array(data, int)

grid = parse_input("/home/mscherbela/develop/advent_of_code/2023/17/input.txt")

def get_possible_moves_part1(s: State, n_rows: int, n_cols: int):
    moves = []
    if s.age < 3:
        moves.append(State(s.r + s.vr, s.c + s.vc, s.vr, s.vc, s.age + 1))
    if abs(s.vr) == 1:
        moves.append(State(s.r, s.c+1, 0, 1, 1))
        moves.append(State(s.r, s.c-1, 0, -1, 1))
    elif abs(s.vc) == 1:
        moves.append(State(s.r+1, s.c, 1, 0, 1))
        moves.append(State(s.r-1, s.c, -1, 0, 1))
    moves = [m for m in moves if (m.r >= 0) and (m.r < n_rows) and (m.c >= 0) and (m.c < n_cols)]
    return moves

def get_possible_moves_part2(s: State, n_rows: int, n_cols: int):
    moves = []
    if s.age < 10:
        moves.append(State(s.r + s.vr, s.c + s.vc, s.vr, s.vc, s.age + 1))
    if s.age >= 4:
        if abs(s.vr) == 1:
            moves.append(State(s.r, s.c+1, 0, 1, 1))
            moves.append(State(s.r, s.c-1, 0, -1, 1))
        elif abs(s.vc) == 1:
            moves.append(State(s.r+1, s.c, 1, 0, 1))
            moves.append(State(s.r-1, s.c, -1, 0, 1))
    moves = [m for m in moves if (m.r >= 0) and (m.r < n_rows) and (m.c >= 0) and (m.c < n_cols)]
    return moves

def bfs(state, grid, get_moves_func):
    known_losses = {state: (0, None)}
    n_rows, n_cols = grid.shape
    frontier = [state]
    found_target = False
    best_known_loss = np.inf
    best_known_end_state = None

    # breadth first search
    while frontier and not found_target:
        state = heapq.heappop(frontier)
        loss = known_losses[state][0]
        if loss + (n_rows - 1 - state.r) + (n_cols - 1 - state.c) > best_known_loss:
            continue
        next_states = get_moves_func(state, n_rows, n_cols)
        for next_state in next_states:
            next_loss = loss + grid[next_state.r, next_state.c]
            if (next_state not in known_losses) or (known_losses[next_state][0] > next_loss):
                known_losses[next_state] = (next_loss, state)
                heapq.heappush(frontier, next_state)
            if (next_state.r == n_rows - 1) and (next_state.c == n_cols - 1):
                if next_loss < best_known_loss:
                    best_known_loss = next_loss
                    best_known_end_state = next_state


    # backtrack
    path = [best_known_end_state]
    while True:
        predecessor = known_losses[path[-1]][1]
        if predecessor is None:
            break
        path.append(predecessor)
    path = path[::-1]
    return best_known_loss, path


plt.close("all")
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
for part, move_func in zip([1, 2], [get_possible_moves_part1, get_possible_moves_part2]):
    state = State(0, 0, 0, 1, 1)
    best_known_loss, path = bfs(state, grid, move_func)
    print(f"Part {part}: {best_known_loss}")

    grid_with_path = grid.copy()
    for state in path:
        grid_with_path[state.r, state.c] = 11
    axes[part-1].imshow(grid_with_path)
    axes[part-1].set_title(f"Part {part}: {best_known_loss}")


