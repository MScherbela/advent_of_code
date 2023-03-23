def get_score(player1, player2):
    score = 1 + player2 # base score for chosen object
    outcome = (player2 - player1) % 3 # 0: draw, 1: win, 2: loss
    score += [3, 6, 0][outcome]
    return score

input_data = []
with open("02/input.txt") as f:
    for l in f:
        l = l.strip()
        if len(l):
            input_data.append(l.split(" "))

# Rock = 0, Paper = 1, Scissors = 2
input_mapping = dict(A=0, B=1, C=2, X=0, Y=1, Z=2)
games = [[input_mapping[x], input_mapping[y]] for x,y in input_data]
total_score = sum([get_score(*g) for g in games])
print(total_score)
