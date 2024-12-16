# %%


def parse_input(fname):
    data = []
    with open(fname) as f:
        for l in f:
            data.append(l.strip())
    return data


def get_neighbours(data, pos):
    r, c = pos
    val = data[r][c]
    rows, cols = len(data), len(data[0])
    neighbours = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    is_connected = []
    for r_n, c_n in neighbours:
        if (0 <= r_n < rows) and (0 <= c_n < cols) and (data[r_n][c_n] == val):
            is_connected.append(True)
        else:
            is_connected.append(False)
    return neighbours, is_connected


def floodfill(data, pos):
    frontier = set([pos])
    is_filled = set([pos])
    fence = set()
    while frontier:
        pos = frontier.pop()
        neighbours, is_connected = get_neighbours(data, pos)
        for n, conn in zip(neighbours, is_connected):
            if conn:
                if n not in is_filled:
                    is_filled.add(n)
                    frontier.add(n)
            else:
                fence.add((pos[0], pos[1], n[0], n[1]))
    return is_filled, fence


def merge_fence(fence):
    n_sides = 0
    while fence:
        f_start = fence.pop()
        if f_start[0] != f_start[2]:
            # between 2 rows
            deltas = [(0, -1), (0, 1)]
        else:
            # between 2 cols
            deltas = [(-1, 0), (1, 0)]

        for dr, dc in deltas:
            f = f_start
            while True:
                neighbour_fence = (f[0] + dr, f[1] + dc, f[2] + dr, f[3] + dc)
                if neighbour_fence in fence:
                    fence.remove(neighbour_fence)
                    f = neighbour_fence
                else:
                    break
        n_sides += 1
    return n_sides


data = parse_input("test_input2.txt")
rows, cols = len(data), len(data[0])
is_processed = set()

part1, part2 = 0, 0
for r in range(rows):
    for c in range(cols):
        pos = (r, c)
        if pos in is_processed:
            continue
        nodes, fence = floodfill(data, pos)
        n_nodes = len(nodes)
        n_fence = len(fence)
        n_sides = merge_fence(fence)

        print(data[r][c], n_nodes, n_fence, n_sides)
        is_processed.update(nodes)
        part1 += n_nodes * n_fence
        part2 += n_nodes * n_sides
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
