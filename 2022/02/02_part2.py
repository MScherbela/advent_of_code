def get_score(player1, player2):
    score = 1 + player2  # base score for chosen object
    outcome = (player2 - player1) % 3  # 0: draw, 1: win, 2: loss
    score += [3, 6, 0][outcome]
    return score


def choose_object(player1, strategy):
    # strategy: 0: lose, 1: draw, 2: win
    offset = [-1, 0, 1][strategy]
    return (player1 + offset) % 3


input_data = []
with open("02/input.txt") as f:
    for l in f:
        l = l.strip()
        if len(l):
            input_data.append(l.split(" "))

# Rock = 0, Paper = 1, Scissors = 2
input_mapping = dict(A=0, B=1, C=2, X=0, Y=1, Z=2)
games = [[input_mapping[x], input_mapping[y]] for x, y in input_data]
games = [[x, choose_object(x, y)] for x, y in games]
total_score = sum([get_score(*g) for g in games])
print(total_score)
