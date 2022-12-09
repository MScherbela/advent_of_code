import numpy as np
import matplotlib.pyplot as plt

data = []
with open("08/input.txt") as f:
    for line in f:
        data.append([int(c) for c in line.strip()])
data = np.array(data, int)
scenic_score = np.ones_like(data)
n_rows, n_cols = data.shape

for i in range(n_rows):
    for j in range(n_cols):
        current_height = data[i,j]

        if (i == 20) and (j==20):
            print(i,j)
            pass

        score = 0 # down
        for k in range(i+1, n_rows):
            score += 1
            if data[k, j] >= current_height:
                break
        scenic_score[i,j] *= score

        score = 0  # up
        for k in range(i-1, -1, -1):
            score += 1
            if data[k, j] >= current_height:
                break
        scenic_score[i, j] *= score

        score = 0 # right
        for k in range(j+1, n_cols):
            score += 1
            if data[i, k] >= current_height:
                break
        scenic_score[i,j] *= score

        score = 0  # left
        for k in range(j-1, -1, -1):
            score += 1
            if data[i, k] >= current_height:
                break
        scenic_score[i, j] *= score

print(np.max(scenic_score))
