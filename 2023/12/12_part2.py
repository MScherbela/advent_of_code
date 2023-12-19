#%%
import time

def get_possible_postfixes(s, groups):
    remaining_strings = []
    g = groups[0]
    i_max = len(s) - sum(groups) - len(groups) + 1 # group size + one dot between each group (-1 for the last)
    for i in range(i_max+1):
        does_fit = '.' not in s[i:i+g] and (i+g == len(s) or s[i+g] != '#')
        if does_fit:
            s_remain = s[i+g+1:]
            if len(groups) > 1 or '#' not in s_remain:
                remaining_strings.append(s_remain)
        if s[i] == '#':
            # If we hit a #, we must place a group here, so we can't continue
            break
    return remaining_strings

def get_nr_of_possible_strings(s, groups, cache):
    if (s, groups) in cache:
        return cache[(s, groups)]
    if len(groups) == 0:
        n = 1
    elif len(groups) == 1:
        n = len(get_possible_postfixes(s, groups))
    else:
        n = 0
        postfixes = get_possible_postfixes(s, groups)
        for postfix in postfixes:
            n += get_nr_of_possible_strings(postfix, groups[1:], cache)
    cache[(s, groups)] = n
    return n
    

def extend_input(symbols, groups, n_reps=5):
    symbols = "?".join([symbols for _ in range(n_reps)])
    groups = groups * n_reps
    return symbols, groups
    
data = []
with open("input.txt") as f:
    for line in f:
        symbols, groups = line.strip().split(" ")
        groups = tuple([int(g) for g in groups.split(",")])
        data.append((symbols, groups))

n_total_part1 = 0
for i, (symbols, groups) in enumerate(data):
     n_total_part1 += get_nr_of_possible_strings(symbols, groups, {})
print("Part 1: ", n_total_part1)

data_extended = [extend_input(symbols, groups) for symbols, groups in data]
n_total_part2 = 0
for i, (symbols, groups) in enumerate(data_extended):
    n_total_part2 += get_nr_of_possible_strings(symbols, groups, {})
print("Part 2: ", n_total_part2)





    



