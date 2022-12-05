n_top = 3
top_calories = [0 for _ in range(n_top)]
calories = 0

with open("01/input.txt") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            if calories > top_calories[0]:
                top_calories = [calories, *top_calories[1:]]
                top_calories = sorted(top_calories)
            calories = 0
        else:
            calories += int(line)
print(sum(top_calories))