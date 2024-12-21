# %%

from functools import lru_cache, cache

PAD_STRING_NUMERIC = "789\n456\n123\n 0A"
PAD_STRING_DIRECTIONAL = " ^A\n<v>"


def get_coords_from_string(pad_string):
    coords = {}
    characters = pad_string.split("\n")
    for r, row in enumerate(characters):
        for c, ch in enumerate(row):
            if ch == " ":
                continue
            coords[ch] = (r, c)
    return coords, characters


def parse_input(fname):
    with open(fname) as f:
        lines = [l.strip() for l in f.readlines()]
    return [l for l in lines if l]


def get_potential_paths(pad_string):
    coords, characters = get_coords_from_string(pad_string)
    potential_paths = {}
    for start, (rs, cs) in coords.items():
        for end, (re, ce) in coords.items():
            paths = set()
            lr_chr = ">" if ce > cs else "<"
            ud_chr = "v" if re > rs else "^"

            # Path 1: UD then LR
            visited_chr = ""
            r, c = rs, cs
            while r != re:
                r -= (rs - re) // abs(rs - re)
                visited_chr += characters[r][c]
            while c != ce:
                c -= (cs - ce) // abs(cs - ce)
                visited_chr += characters[r][c]
            if " " not in visited_chr:
                paths.add(ud_chr * abs(re - rs) + lr_chr * abs(ce - cs) + "A")

            # Path 2:LR then UD
            visited_chr = ""
            r, c = rs, cs
            while c != ce:
                c -= (cs - ce) // abs(cs - ce)
                visited_chr += characters[r][c]
            while r != re:
                r -= (rs - re) // abs(rs - re)
                visited_chr += characters[r][c]
            if " " not in visited_chr:
                paths.add(lr_chr * abs(ce - cs) + ud_chr * abs(re - rs) + "A")

            potential_paths[(start, end)] = list(paths)
    return potential_paths


potential_paths = get_potential_paths(PAD_STRING_NUMERIC) | get_potential_paths(PAD_STRING_DIRECTIONAL)


@cache
def get_cost_of_path(path, level=0, final_level=3):
    if level == final_level:
        return len(path)
    cost = 0
    s = "A"
    for e in path:
        cost += _get_cost_of_step(s, e, level, final_level)
        s = e
    return cost


@cache
def _get_cost_of_step(start, end, level, final_level=3):
    costs = []
    for path in potential_paths[(start, end)]:
        costs.append(get_cost_of_path(path, level + 1, final_level))
    return min(costs)


lines = parse_input("input.txt")

part1 = 0
part2 = 0
for line in lines:
    cost1 = get_cost_of_path(line, final_level=3)
    cost2 = get_cost_of_path(line, final_level=26)
    numeric_part = int(line.replace("A", ""))
    part1 += cost1 * numeric_part
    part2 += cost2 * numeric_part
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
