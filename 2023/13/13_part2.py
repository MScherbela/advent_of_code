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
    original_mirror_col = 0
    fixed_mirror_col = 0
    for mirror_col in range(1, n_cols):
        errors_per_row = []
        for row in pos_per_row:
            dist_left = mirror_col - row
            dist_right = row - mirror_col + 1
            dist_max = min(mirror_col, n_cols - mirror_col)
            dist_left = dist_left[(dist_left > 0) & (dist_left <= dist_max)]
            dist_right = dist_right[(dist_right > 0) & (dist_right <= dist_max)]
            len_r, len_l = len(dist_right), len(dist_left)
            if len_r == len_l:
                if np.any(dist_left != dist_right[::-1]):
                    errors_per_row.append(2)
                else:
                    errors_per_row.append(0)
            elif len_r == len_l + 1:
                if all([x in dist_right for x in dist_left]):
                    errors_per_row.append(1)
                else:
                    errors_per_row.append(2)
            elif len_l == len_r + 1:
                if all([x in dist_left for x in dist_right]):
                    errors_per_row.append(1)
                else:
                    errors_per_row.append(2)
            else:
                errors_per_row.append(2)

        total_errors = sum(errors_per_row)
        if total_errors == 0:
            original_mirror_col = mirror_col
        elif total_errors == 1:
            fixed_mirror_col = mirror_col
    return original_mirror_col, fixed_mirror_col

total_part1 = 0
total_part2 = 0
for p in patterns:
    rock_pos_per_row = [np.where(row)[0] for row in p]
    rock_pos_per_col = [np.where(row)[0] for row in p.T]
    n_col_orig, n_col_fixed = get_reflection_col_nr(rock_pos_per_row, p.shape[1])
    n_row_orig, n_row_fixed = get_reflection_col_nr(rock_pos_per_col, p.shape[0])
    assert n_col_orig + n_row_orig > 0
    assert n_col_fixed + n_row_fixed > 0
    total_part1 += n_col_orig + 100 * n_row_orig
    total_part2 += n_col_fixed + 100 * n_row_fixed
print("Part 1: ", total_part1)
print("Part 2: ", total_part2)


