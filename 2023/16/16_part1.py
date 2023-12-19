#%%
with open("input.txt") as f:
    grid = [l.strip() for l in f.readlines()]
    

def propagate_beam(x, y, vx, vy, c):
    if (c == '.') or ((c == '|') and (vx == 0)) or ((c == '-') and (vy == 0)):
        return [(x+vx, y+vy, vx, vy)]
    elif c == '/':
        vx_new = -vy
        vy_new = -vx
        return [(x+vx_new, y+vy_new, vx_new, vy_new)]
    elif c == "\\":
        vx_new = vy
        vy_new = vx
        return [(x+vx_new, y+vy_new, vx_new, vy_new)]
    elif c == '|':
        return [(x, y+1, 0, 1), (x, y-1, 0, -1)]
    elif c == '-':
        return [(x+1, y, 1, 0), (x-1, y, -1, 0)]
    
def get_n_energized(grid, starting_state):
    n_rows = len(grid)
    n_cols = len(grid[0])
    frontier = [starting_state]
    has_been_visited = set()
    while frontier:
        state = frontier.pop()
        has_been_visited.add(state)
        for new_state in propagate_beam(*state, grid[state[1]][state[0]]):
            if (new_state[0] < 0) or (new_state[0] >= n_cols) or (new_state[1] < 0) or (new_state[1] >= n_rows):
                continue
            if new_state not in has_been_visited:
                frontier.append(new_state)
    energized_tiles = set([(x, y) for (x, y, _, _) in has_been_visited])
    return len(energized_tiles)

n_part1 = get_n_energized(grid, (0, 0, 1, 0))
print("Part 1: ", n_part1)

n_rows = len(grid)
n_cols = len(grid[0])

energies = {}
for row in range(n_rows):
    starting_states = [(0, row, 1, 0), (n_cols-1, row, -1, 0)]
    for state in starting_states:
        energies[state] = get_n_energized(grid, state)

for col in range(n_cols):
    starting_states = [(col, 0, 0, 1), (col, n_rows-1, 0, -1)]
    for state in starting_states:
        energies[state] = get_n_energized(grid, state)

max_energy = max(energies.values())




