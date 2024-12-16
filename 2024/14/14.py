# %%
import parse
import numpy as np
import matplotlib.pyplot as plt


def parse_input(fname):
    pos = []
    v = []
    with open(fname) as f:
        for l in f:
            result = parse.parse("p={x:d},{y:d} v={vx:d},{vy:d}", l.strip())
            pos.append([result["x"], result["y"]])
            v.append([result["vx"], result["vy"]])
    return np.array(pos), np.array(v)


fname = "input.txt"
pos, v = parse_input(fname)
if fname == "test_input.txt":
    x_max, y_max = 11, 7
else:
    x_max, y_max = 101, 103


n_steps = 100

pos_final = (pos + n_steps * v) % np.array([x_max, y_max])

is_left = pos_final[:, 0] < x_max // 2
is_top = pos_final[:, 1] < y_max // 2
is_right = pos_final[:, 0] > x_max // 2
is_bottom = pos_final[:, 1] > y_max // 2

n1 = np.sum(is_left & is_top)
n2 = np.sum(is_right & is_top)
n3 = np.sum(is_left & is_bottom)
n4 = np.sum(is_right & is_bottom)
part1 = n1 * n2 * n3 * n4
print(f"Part 1: {part1}")

metrics = []
for i in range(10_000):
    print(i)
    pos_final = (pos + i * v) % np.array([x_max, y_max])
    distances = np.linalg.norm(pos_final[:, None, :] - pos_final, axis=-1)
    metrics.append([np.quantile(distances, 0.2), np.mean(distances), np.quantile(distances, 0.8)])
metrics = np.array(metrics)

plt.close("all")
plt.plot(metrics)

# %%
plt.figure()
n_steps_values = [7055]

for i in n_steps_values:
    print(i)
    pos_final = (pos + i * v) % np.array([x_max, y_max])
    plt.clf()
    plt.title(f"Step {i}")
    plt.scatter(pos_final[:, 0], pos_final[:, 1])
    plt.savefig(f"step_{i:03d}.png", dpi=50)
