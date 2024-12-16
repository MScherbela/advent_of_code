# %%
import numpy as np
import matplotlib.pyplot as plt


def parse_input(fname):
    walls = set()
    boxes = {}
    moves = ""
    pos = None
    rows, cols = 0, 0
    with open(fname) as f:
        for i, l in enumerate(f):
            l = l.strip()
            if "#" in l or "." in l or "O" in l:
                for j, c in enumerate(l):
                    if c == "#":
                        walls.add((i, 2 * j))
                        walls.add((i, 2 * j + 1))
                    elif c == "O":
                        boxes[(i, 2 * j)] = (i, 2 * j)
                        boxes[(i, 2 * j + 1)] = (i, 2 * j)
                    elif c == "@":
                        pos = (i, 2 * j)
                rows += 1
                cols = j + 1
            else:
                moves = moves + l
    return walls, boxes, pos, moves, (rows, 2 * cols)


def can_move(walls, boxes, pos, dir):
    next_pos = tuple(pos + dir)
    if next_pos in walls:
        return False, set()
    if next_pos in boxes:
        return can_move_box(walls, boxes, boxes[next_pos], dir)
    return True, set()


def can_move_box(walls, boxes, pos, dir):
    next_positions = [(pos[0] + dir[0], pos[1] + dir[1]), (pos[0] + dir[0], pos[1] + dir[1] + 1)]
    if any(p in walls for p in next_positions):
        return False, set()
    do_move = True
    boxes_to_move = set([pos])
    for p in next_positions:
        if p in boxes:
            if boxes[p] == pos:
                # this is the box we are trying to move, ignore
                continue
            do_move_, boxes_to_move_ = can_move_box(walls, boxes, boxes[p], dir)
            do_move = do_move and do_move_
            boxes_to_move.update(boxes_to_move_)
    return do_move, boxes_to_move


def step(walls, boxes, pos, dir):
    dr, dc = dir
    do_move, boxes_to_update = can_move(walls, boxes, pos, dir)
    if do_move:
        pos = (pos[0] + dr, pos[1] + dc)
        for b in boxes_to_update:
            del boxes[b]
            del boxes[(b[0], b[1] + 1)]
        for b in boxes_to_update:
            b_new = (b[0] + dr, b[1] + dc)
            boxes[b_new] = b_new
            boxes[(b_new[0], b_new[1] + 1)] = b_new
    assert pos not in boxes
    assert pos not in walls
    return pos


def render(walls, boxes, pos, shape, fname):
    grid = np.zeros(shape)
    for r, c in walls:
        grid[r, c] = 1
    for r, c in boxes:
        grid[r, c] = 2
    grid[pos[0], pos[1]] = 3

    plt.close("all")
    plt.imshow(grid)
    plt.title(fname)
    plt.savefig(fname, dpi=100)
    return grid


walls, boxes, pos, moves, shape = parse_input("input.txt")
moves_to_dir = {"<": np.array([0, -1]), ">": np.array([0, 1]), "^": np.array([-1, 0]), "v": np.array([1, 0])}
render(walls, boxes, pos, shape, f"step_{0:03d}.png")
for i, m in enumerate(moves):
    if i == 77:
        pass
    dir = moves_to_dir[m]
    pos = step(walls, boxes, pos, dir)
render(walls, boxes, pos, shape, f"step_{i+1:03d}.png")
box_coords = set(boxes.values())
part2 = 0
for r, c in box_coords:
    part2 += 100 * r + c
print(f"Part 2: {part2}")
