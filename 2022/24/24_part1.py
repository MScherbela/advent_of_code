import numpy as np
import matplotlib.pyplot as plt

def to_grid(blizzards, walls, frontier, height, width):
    grid = np.zeros([height, width], int)
    for w in walls:
        grid[w[0], w[1]] = -5
    for b in blizzards:
        grid[b[0], b[1]] = -len(blizzards[(b[0], b[1])])
    for f in frontier:
        grid[f[0], f[1]] = 3
    return grid


def parse_input(fname):
    with open(fname) as f:
        blizzards = {}
        walls = set()
        for row, line in enumerate(f):
            line = line.strip()
            for col,c in enumerate(line):
                pos = (row, col)
                if c in '<>^v':
                    if pos not in blizzards:
                        blizzards[pos] = []
                    blizzards[pos].append(c)
                elif c == '#':
                    walls.add(pos)
            if '##' in line:
                if row == 0:
                    start_pos = (row, [col for col, c in enumerate(line) if c == '.'][0])
                else:
                    end_pos = (row, [col for col, c in enumerate(line) if c == '.'][0])
        width = len(line)
        height = row + 1
    return blizzards, walls, start_pos, end_pos, height, width

def move_blizzards(blizzards, height, width):
    new_blizzards = {}
    for pos, directions in blizzards.items():
        for direction in directions:
            row, col = pos
            if direction == '>':
                col += 1
            elif direction == '<':
                col -= 1
            elif direction == '^':
                row -= 1
            elif direction == 'v':
                row += 1
            row = (row - 1) % (height - 2) + 1
            col = (col - 1) % (width - 2) + 1
            new_pos = (row, col)
            if new_pos not in new_blizzards:
                new_blizzards[new_pos] = []
            new_blizzards[new_pos].append(direction)
    return new_blizzards

blizzards, walls, start_pos, end_pos,height, width = parse_input("24/input.txt")

def get_shortest_duration(blizzards, walls, start_pos, end_pos, height, width):
    t = 0
    frontier = {start_pos}
    while end_pos not in frontier:
        new_frontier = set()
        blizzards = move_blizzards(blizzards, height, width)
        for pos in frontier:
            for delta in [(0,0), (0,1), (0,-1), (1,0), (-1,0)]:
                new_pos = (pos[0]+delta[0], pos[1]+delta[1])
                if (new_pos not in walls) and (new_pos not in blizzards) and (new_pos[0] >= 0):
                    new_frontier.add(new_pos)
        frontier = new_frontier
        t += 1
    return t, frontier, blizzards


t1, frontier, blizzards = get_shortest_duration(blizzards, walls, start_pos, end_pos, height, width)
t2, frontier, blizzards = get_shortest_duration(blizzards, walls, end_pos, start_pos, height, width)
t3, frontier, blizzards = get_shortest_duration(blizzards, walls, start_pos, end_pos, height, width)

print("Part 1", t1)
print("Part 2", t1+t2+t3)

#
# grid = to_grid(blizzards, walls, frontier, height, width)
# plt.close("all")
# plt.imshow(grid, cmap='bwr', clim=[-5,5])







