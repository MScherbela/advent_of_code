#%%
import numpy as np

def parse_input(fname):
    pos_data = []
    v_data = []
    with open(fname) as f:
        for line in f:
            pos, v = line.strip().split('@')
            pos_data.append([int(x) for x in pos.split(',')])
            v_data.append([int(x) for x in v.split(',')])
    return np.array(pos_data), np.array(v_data)

def get_intersection(p1, v1, p2, v2):
    V = np.array([v1, v2]).T
    if np.linalg.det(V) == 0:
        return np.nan, np.array([np.nan, np.nan])
    t_intersec = np.linalg.solve(V, p2 - p1)
    t_intersec[1] *= -1
    return t_intersec, p1 + t_intersec[0] * v1

pos, v = parse_input("/home/mscherbela/develop/advent_of_code/2023/24/input.txt")

np.set_printoptions(precision=2, suppress=True)
pos_min = 200000000000000
pos_max = 400000000000000
# pos_min = 7
# pos_max = 27

n_intersections = 0
for ind1, (p1, v1) in enumerate(zip(pos, v)):
    for ind2, (p2, v2) in enumerate(zip(pos, v)):
        if ind1 >= ind2:
            continue
        t, intersec = get_intersection(p1[:2], v1[:2], p2[:2], v2[:2])
        if np.all(t > 0) and np.all(intersec >= pos_min) and np.all(intersec <= pos_max):
            n_intersections += 1
print(n_intersections)


