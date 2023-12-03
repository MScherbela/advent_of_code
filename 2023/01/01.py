import re
#%%

# Part 1
total = 0
with open("input.txt", "r") as f:
    for line in f:
        digits = [c for c in line.strip() if c.isdigit()]
        first = digits[0]
        last = digits[-1]
        total += int(first+last)
print(total)

#%%
# Part 2
def to_digit(s):
    if s.isdigit():
        return s
    else:
        return str(digit_words.index(s) + 1)
digit_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digit_regex = r"(\d|" + r"|".join(digit_words) + r")"

total = 0
with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        m = re.search(digit_regex + ".*" + digit_regex, line.strip())
        if m is not None:
            total += int(to_digit(m.group(1)) + to_digit(m.group(2)))
        else:
            m = re.search(digit_regex, line)
            total += int(to_digit(m.group(1)) * 2)
print(total)
