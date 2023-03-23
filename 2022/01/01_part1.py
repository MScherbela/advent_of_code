max_calories = 0
calories = 0

with open("01/input.txt") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            max_calories = max(calories, max_calories)
            calories = 0
        else:
            calories += int(line)
print(max_calories)