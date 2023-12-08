#%%
from math import sqrt, floor, ceil

def parse_input(fname):
    with open(fname) as f:
        times = f.readline().strip().split(":")[1].split(" ")
        distances = f.readline().strip().split(":")[1].split(" ")
        times_parsed = [int(x) for x in times if len(x)]
        distances_parsed = [int(x) for x in distances if len(x)]

        distance_merged = "".join(distances).replace(" ", "")
        time_merged = "".join(times).replace(" ", "")
        races = [(t, d) for (t, d) in zip(times_parsed, distances_parsed)]

        return races, int(time_merged), int(distance_merged)
    
def get_n_ways_to_win(t, d):
    # d = v * (t - tc) = tc * (t-tc)
    # tc**2 - t*tc + d = 0
    # tc = t/2 +- sqrt((t/2)**2 - d)
    tmin = t/2 - sqrt((t/2)**2 - d)
    tmax = t/2 + sqrt((t/2)**2 - d)
    tmin = int(floor(tmin)) + 1
    tmax = int(ceil(tmax)) - 1
    n_ways_to_win = tmax - tmin + 1
    return n_ways_to_win
    
races, T, D = parse_input("input.txt")


margin_total = 1
for t, d in races:
    n_ways_to_win = get_n_ways_to_win(t, d)
    margin_total *= n_ways_to_win

print(margin_total)
print(get_n_ways_to_win(T, D))