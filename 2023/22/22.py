# %%
import numpy as np
import copy


class Brick:
    def __init__(self, xmin, xmax):
        self.xmin = xmin
        self.xmax = xmax

    @classmethod
    def from_string(cls, s):
        xmin, xmax = s.split("~")
        coords_min = np.array([int(x) for x in xmin.split(",")], dtype=np.int32)
        coords_max = np.array([int(x) for x in xmax.split(",")], dtype=np.int32)
        return cls(coords_min, coords_max)

    def __repr__(self):
        return f"Brick({self.xmin} - {self.xmax})"


def parse_input(fname):
    bricks = []
    for line in open(fname):
        bricks.append(Brick.from_string(line.strip()))
    return bricks


def get_supporters_below(bricks, xy_overlaps):
    """Get indices of bricks, that support each brick."""
    supports = []
    for i, b in enumerate(bricks):
        supports.append([])
        for j in xy_overlaps[i]:
            if bricks[j].xmax[2] == b.xmin[2] - 1:
                supports[-1].append(j)
    return supports


def settle_step(bricks, xy_overlaps):
    n_moves = 0
    for i, b in enumerate(bricks):
        if b.xmin[2] == 1:
            continue  # on the ground

        steps_to_move = b.xmin[2] - 1
        for j in xy_overlaps[i]:
            steps_to_move = min(steps_to_move, b.xmin[2] - bricks[j].xmax[2] - 1)
            if steps_to_move == 0:
                break
        if steps_to_move > 0:
            b.xmin[2] -= steps_to_move
            b.xmax[2] -= steps_to_move
            b.has_moved = True
            n_moves += 1
    return n_moves


bricks = parse_input("input.txt")
xy_overlaps = []

print("Computing overlaps")
for i, b1 in enumerate(bricks):
    xy_overlaps.append([])
    for j, b2 in enumerate(bricks):
        if i == j:
            continue
        overlaps_x = (b1.xmax[0] >= b2.xmin[0]) and (b1.xmin[0] <= b2.xmax[0])
        overlaps_y = (b1.xmax[1] >= b2.xmin[1]) and (b1.xmin[1] <= b2.xmax[1])
        b1_is_higher = b1.xmin[2] > b2.xmin[2]
        if overlaps_x and overlaps_y and b1_is_higher:
            xy_overlaps[-1].append(j)
xy_overlaps = [np.array(o, np.int32) for o in xy_overlaps]

print("Settling bricks")
while settle_step(bricks, xy_overlaps):
    pass

print("Counting safe bricks")
supports = get_supporters_below(bricks, xy_overlaps)
is_required = np.zeros(len(bricks), dtype=np.bool)
for s in supports:
    if len(s) == 1:
        # This brick is only supported by a single other brick, so this other brick is required
        is_required[s[0]] = True

n_safe_to_disintegrate = np.sum(~is_required)
print(f"Part 1: {n_safe_to_disintegrate}")

n_others_moved = np.zeros(len(bricks), dtype=np.int32)
for i in range(len(bricks)):
    # We do not need to check safe bricks
    if not is_required[i]:
        continue

    bricks_subset = copy.deepcopy(bricks)
    xy_overlaps_subset = copy.deepcopy(xy_overlaps)
    bricks_subset.pop(i)
    xy_overlaps_subset.pop(i)
    xy_overlaps_subset = [o[o != i] for o in xy_overlaps_subset]
    xy_overlaps_subset = [o - (o > i) for o in xy_overlaps_subset]
    for b in bricks_subset:
        b.has_moved = False

    while settle_step(bricks_subset, xy_overlaps_subset):
        pass
    n_others_moved[i] = np.sum([b.has_moved for b in bricks_subset])
    print(f"Brick {i} disintegrated: {n_others_moved[i]} moved")
print(sum(n_others_moved))
