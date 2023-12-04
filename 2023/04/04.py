#%%
def parse_data(fname):
    data = []
    with open(fname, "r") as f:
        for line in f:
            line = line.strip()
            line = line.split(":")[1]
            winning, have = line.split("|")
            winning = [int(x) for x in winning.split(" ") if len(x)]
            have = [int(x) for x in have.strip().split(" ") if len(x)]
            data.append((winning, have))
    return data

data = parse_data("input.txt")
n_copies = [1 for _ in data]

points = 0
for ind_current, (winning, have) in enumerate(data):
    n_winning = len(set(winning).intersection(set(have)))

    # Scoring for part 1
    if n_winning:
        points += 2**(n_winning - 1)

    # Scoring for part 2
    for i in range(ind_current+1, min(len(data), ind_current+1+n_winning)):
        n_copies[i] += n_copies[ind_current]

print(points)
print(sum(n_copies))