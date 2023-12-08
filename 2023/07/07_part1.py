#%%
from collections import Counter

CARD_RANKING = {c:i for i, c in enumerate("23456789TJQKA")}

def get_figure(hand):
    counts = sorted(Counter(hand).values(), reverse=True)
    if counts[0] == 5:
        return 6
    elif counts[0] == 4:
        return 5
    elif counts[0] == 3 and counts[1] == 2:
        return 4
    elif counts[0] == 3:
        return 3
    elif counts[0] == 2 and counts[1] == 2:
        return 2
    elif counts[0] == 2:
        return 1
    else:
        return 0
    
def rate_hand(hand):
    return (get_figure(hand), *[CARD_RANKING[c] for c in hand])

hands = []
with open("input.txt") as f:
    for line in f:
        hand, bid = line.strip().split(" ")
        hands.append((hand, int(bid)))

hands = sorted(hands, key=lambda x: rate_hand(x[0]))
total_score = 0
for i, (hand, bid) in enumerate(hands):
    total_score += bid * (i+1)
    print(hand, bid, i+1)
print(total_score)



