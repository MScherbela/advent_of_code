#%%
with open("input.txt") as f:
    data = []
    for line in f:
        line = [int(x) for x in line.strip().split(" ")]
        data.append(line)

total_part1 = 0
total_part2 = 0
for row in data:
    is_all_0 = False
    final_value = [row[-1]]
    first_value = [row[0]]
    while not is_all_0:
        differences = []
        is_all_0 = True
        for i in range(len(row)-1):
            d = row[i+1] - row[i]
            differences.append(d)
            if d != 0:
                is_all_0 = False
        final_value.append(differences[-1])
        first_value.append(differences[0])
        row = differences

    # Get forward prediction
    prediction_final = sum(final_value)
    total_part1 += prediction_final

    # Get backward prediction
    prediction_first = 0
    for v in reversed(first_value):
        prediction_first = v - prediction_first
    total_part2 += prediction_first
    
print(f"Part 1: {total_part1}")        
print(f"Part 2: {total_part2}")        

            
            