#%%
import numpy as np

def parse_input(fname):
    data = []
    for line in open(fname):
        line = line.strip()
        tokens = line.split(" ")
        data.append((tokens[0], int(tokens[1]), tokens[2][2:-1]))
    return data

def to_vector_part1(dir, l):
    if dir == "R":
        v = np.array([1, 0], int)
    elif dir == "L":
        v = np.array([-1, 0], int)
    elif dir == "U":
        v = np.array([0, 1], int)
    elif dir == "D":
        v = np.array([0, -1], int)
    return v*l

def to_vector_part2(hex_string):
    l = int(hex_string[:-1], 16)
    if hex_string[-1] == "0":
        v = np.array([1, 0], int)
    elif hex_string[-1] == "1":
        v = np.array([0, -1], int)
    elif hex_string[-1] == "2":
        v = np.array([-1, 0], int)
    elif hex_string[-1] == "3":
        v = np.array([0, 1], int)
    return v*l

def get_area(vectors):
    vertices = np.cumsum(vectors, axis=0)
    boundary_length = np.sum(np.abs(vectors))

    A = 0
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = vertices[(i+1)%len(vertices)]
        A += v1[0] * v2[1] - v1[1] * v2[0]
    A = abs(A) // 2
    A_total = abs(A) + boundary_length // 2 + 1
    return A_total


data = parse_input("/home/mscherbela/develop/advent_of_code/2023/18/input.txt")
movements1 = [to_vector_part1(dir, l) for dir, l, _ in data]
A1 = get_area(movements1)
print("Part 1: ", A_total)

movements2 = [to_vector_part2(hex_string) for _, _, hex_string in data]
A2 = get_area(movements2)
print("Part 2: ", A2)




# plt.close("all")
# plt.plot(vertices[:, 0], vertices[:, 1], 'k', marker='o')
# plt.plot([vertices[0, 0], vertices[-1, 0]], [vertices[0, 1], vertices[-1, 1]], 'k', marker='o')
# plt.axis("equal")
# plt.grid()

# vmin = vertices.min(axis=0)
# vmax = vertices.max(axis=0)
# plt.xticks(np.arange(vmin[0]-1, vmax[0]+2))
# plt.yticks(np.arange(vmin[1]-1, vmax[1]+2))
# plt.xlim(vmin[0]-1, vmax[0]+1)
# plt.ylim(vmin[1]-1, vmax[1]+1)


