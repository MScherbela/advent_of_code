#%%
import numpy as np

def parse_input(fname):
    patterns = [[]]
    for line in open(fname):
        if line.strip() == "":
            patterns.append([])
        else:
            patterns[-1].append([0 if c == '.' else 1 for c in line.strip()])
    return [np.array(p, int) for p in patterns]

patterns = parse_input("input.txt")


def get_reflection_col_nr(pos_per_row, n_cols):
    for mirror_col in range(1, n_cols):
        is_mirror_col = True
        for row in pos_per_row:
            dist_left = mirror_col - row
            dist_right = row - mirror_col + 1
            dist_max = min(mirror_col, n_cols - mirror_col)
            dist_left = dist_left[(dist_left > 0) & (dist_left <= dist_max)]
            dist_right = dist_right[(dist_right > 0) & (dist_right <= dist_max)]

            if (len(dist_left) != len(dist_right)) or np.any(dist_left != dist_right[::-1]):
                is_mirror_col = False
                break
        if is_mirror_col:
            return mirror_col
    return 0

total_part1 = 0
for p in patterns:
    rock_pos_per_row = [np.where(row)[0] for row in p]
    rock_pos_per_col = [np.where(row)[0] for row in p.T]
    n_col = get_reflection_col_nr(rock_pos_per_row, p.shape[1])
    n_row = get_reflection_col_nr(rock_pos_per_col, p.shape[0])
    assert n_col + n_row > 0
    total_part1 += n_col + 100 * n_row
print("Part 1: ", total_part1)


