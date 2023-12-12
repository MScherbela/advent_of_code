#%%
import numpy as np

def parse_input(fname):
    with open(fname) as f:
        data = [l.strip() for l in f.readlines()]
        data = [[(c == "#") for c in r] for r in data]
    return np.array(data)

img = parse_input("input.txt")
metric_rows = np.ones(img.shape[0], dtype=int)
metric_cols = np.ones(img.shape[1], dtype=int)

# Part 1: 2
# Part 2: 1_000_000
expansion = 1_000_000

for row in range(img.shape[0]):
    if not np.any(img[row]):
        metric_rows[row] = expansion

for col in range(img.shape[1]):
    if not np.any(img[:, col]):
        metric_cols[col] = expansion

galaxies = np.stack(np.where(img), axis=1)
n_galaxies = len(galaxies)

distances = []
for i1 in range(n_galaxies):
    for i2 in range(i1+1, n_galaxies):
        d = 0
        row, col = galaxies[i1]
        row_tgt, col_tgt = galaxies[i2]
        while row != row_tgt:
            d += metric_rows[row]
            row += np.sign(row_tgt - row)
        while col != col_tgt:
            d += metric_cols[col]
            col += np.sign(col_tgt - col)
        distances.append(d)

print("Sum of distances: ", sum(distances))


            
        
