#%%
COLOR_MAPPING = {"red": 0, "green": 1, "blue": 2}

def parse_input(fname):
    with open(fname, "r") as f:
        games = []
        for line in f:
            line = line.strip().split(":")[1]
            round_strings = line.split(";")
            rounds = []
            for round_string in round_strings:
                color_strings = round_string.strip().split(",")
                n_per_color = [0, 0, 0]
                for color_string in color_strings:
                    color_string = color_string.strip()
                    n, color = color_string.split(" ")
                    n_per_color[COLOR_MAPPING[color]] = int(n)
                rounds.append(n_per_color)
            games.append(rounds)
    return games

n_per_color = [12, 13, 14]
games = parse_input("input.txt")

sum_of_ids = 0
sum_of_powers = 0
for ind_game, game in enumerate(games):
    is_possible = True
    n_cubes_min = [0, 0, 0]
    for round in game:
        for i in range(3):
            if round[i] > n_per_color[i]:
                is_possible = False
            n_cubes_min[i] = max(n_cubes_min[i], round[i])
    if is_possible:
        sum_of_ids += (ind_game+1)
    power = n_cubes_min[0] * n_cubes_min[1] * n_cubes_min[2]
    sum_of_powers += power

print(f"Sum of IDs (part 1)   : {sum_of_ids}")
print(f"Sum of powers (part 2): {sum_of_powers}")

