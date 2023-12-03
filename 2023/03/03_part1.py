#%%
def is_symbol(c):
    return (c != '.') and (not c.isdigit())

with open("input.txt", "r") as f:
    data = f.read().splitlines()

n_rows = len(data)
n_cols = len(data[0])
total_of_part_nrs = 0
all_nrs = []
nr_grid = [[-1 for _ in range(n_cols)] for _ in range(n_rows)]

gear_positions = []

nr_index = 0
for row in range(n_rows):
    col = 0

    while col < n_cols:
        # Go to next number
        while (col < n_cols) and not data[row][col].isdigit():
            if data[row][col] == '*':
                gear_positions.append((row, col))
            col += 1
        if col == n_cols:
            continue

        # Get nr
        col_start = col
        nr_string = ""
        while (col < n_cols) and data[row][col].isdigit():
            nr_string += data[row][col]
            nr_grid[row][col] = nr_index
            col += 1
        col_end = col -1
        all_nrs.append(int(nr_string))
        nr_index += 1

        # Check surroundings
        is_surrounded_by_symbol = False
        for r in range(max(0, row-1), min(n_rows, row+2)):
            for c in range(max(0, col_start-1), min(n_cols, col_end+2)):
                if is_symbol(data[r][c]):
                    is_surrounded_by_symbol = True
                    break
        
        if is_surrounded_by_symbol:
            total_of_part_nrs += int(nr_string)

total_of_gear_ratios = 0
for row, col in gear_positions:
    adjacent_nrs = {}
    for r in range(max(0, row-1), min(n_rows, row+2)):
        for c in range(max(0, col-1), min(n_cols, col+2)):
            if nr_grid[r][c] != -1:
                adjacent_nrs[nr_grid[r][c]] = all_nrs[nr_grid[r][c]]
    if len(adjacent_nrs) == 2:
        nrs = list(adjacent_nrs.values())
        total_of_gear_ratios += nrs[0] * nrs[1]

           
print(f"Total of part nrs (part 1)   : {total_of_part_nrs}")
print(f"Total of gear ratios (part 2): {total_of_gear_ratios}")

        
    


