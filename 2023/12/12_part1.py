#%%
import re

def build_regex(groups):
    regex_for_groups = [f"[#\\?]{{{g}}}" for g in groups]
    regex_for_delimiter = "[\.\\?]+"
    regex_for_beg_end = "[\\.\\?]*"

    regex = regex_for_beg_end + regex_for_delimiter.join(regex_for_groups) + regex_for_beg_end
    regex = "^" + regex + "$"
    return re.compile(regex)

def get_nr_of_possible_strings(s, group_regex):
    if group_regex.match(s) is None:
        return 0
    ind_question_mark = s.find("?")
    if ind_question_mark == -1:
        return 1
    else:
        s1 = s[:ind_question_mark] + "#" + s[ind_question_mark+1:]
        s2 = s[:ind_question_mark] + "." + s[ind_question_mark+1:]
        return get_nr_of_possible_strings(s1, group_regex) + get_nr_of_possible_strings(s2, group_regex)
    
def extend_input(symbols, groups, n_reps=5):
    symbols = "?".join([symbols for _ in range(n_reps)])
    groups = groups * n_reps
    return symbols, groups

data = []
with open("test_input.txt") as f:
    for line in f:
        symbols, groups = line.strip().split(" ")
        groups = [int(g) for g in groups.split(",")]
        data.append((symbols, groups))

n_total_part1 = 0
for i, (symbols, groups) in enumerate(data):
    regex = build_regex(groups)
    n_total_part1 += get_nr_of_possible_strings(symbols, regex)
print("Part 1: ", n_total_part1)

data_extended = [extend_input(symbols, groups) for symbols, groups in data]
n_total_part2 = 0
for i, (symbols, groups) in enumerate(data_extended):
    regex = build_regex(groups)
    n_total_part2 += get_nr_of_possible_strings(symbols, regex)

print("Part 2: ", n_total_part2)



