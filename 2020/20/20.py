import numpy as np

def parse_input(fname):
    tiles = {}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if 'Tile' in line:
                id = int(line.replace("Tile ", "").replace(":", ""))
                tile = []
            elif len(line) > 0:
                tile.append([1 if c == '#' else 0 for c in line])
            else:
                tiles[id] = np.array(tile, int)
        if id not in tiles:
            tiles[id] = np.array(tile, int)
    return tiles

def get_border_hash(values):
    values = tuple(values)
    return min(values, values[::-1])

def add_entry(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)

tiles = parse_input("2020/20/input.txt")
borders = {}
for id, t in tiles.items():
    h = get_border_hash(t[0, :])
    add_entry(borders, get_border_hash(t[0, :]), (id, 0))
    add_entry(borders, get_border_hash(t[:, -1]), (id, 1))
    add_entry(borders, get_border_hash(t[-1, :]), (id, 1))
    add_entry(borders, get_border_hash(t[:, 0]), (id, 3))

edge_count = {}
for k,v in borders.items():
    if len(v) == 2:
        continue
    if len(v) == 1:
        id = v[0][0]
        if id not in edge_count:
            edge_count[id] = 1
        else:
            edge_count[id] += 1
    else:
        raise ValueError("Triple match")
corner_ids = [k for k,v in edge_count.items() if v == 2]
print(corner_ids)
print(np.prod(corner_ids))
