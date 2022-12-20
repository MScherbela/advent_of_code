def shift_element(data, pos, shift):
    element = data[pos]
    new_pos = (pos + shift) % (len(data) - 1)
    data = data[:pos] + data[pos+1:]
    data = data[:new_pos] + [element] + data[new_pos:]
    return data


def mix_data(data, original_position=None):
    N = len(data)
    original_position = original_position or [i for i in range(N)]
    for pos_orig in range(N):
        pos = original_position.index(pos_orig)
        shift = data[pos]
        data = shift_element(data, pos, shift)
        original_position = shift_element(original_position, pos, shift)
    return data, original_position

with open("20/input.txt") as f:
    data = f.read().split("\n")
    data = [int(x) for x in data]

# part 1
decryption_key = 1
n_rounds = 1
#
# part 2
decryption_key = 811589153
n_rounds = 10

data = [x * decryption_key for x in data]

original_position = None
for n in range(n_rounds):
    data, original_position = mix_data(data, original_position)

pos_zero = data.index(0)
output = 0
for offset in [1000, 2000, 3000]:
    output += data[(pos_zero + offset) % len(data)]
print(output)




