import numpy as np

BASE = 5
SNAFU_DIGITS = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2, 0: '0', 1: '1', 2: '2', -1: '-', -2: '='}

def parse_input(fname):
    numbers = []
    with open(fname) as f:
        for line in f:
            numbers.append(line.strip())
    return numbers

def to_decimal(snafu: str):
    factor = 1
    result = 0
    for c in snafu[::-1]:
        result += factor * SNAFU_DIGITS[c]
        factor *= BASE
    return result


def to_snafu(decimal: int):
    factor = 1
    while abs(decimal) > (BASE // 2) * factor:
        factor *= BASE

    snafu = ""
    while factor >= 1:
        digit = int(np.round(decimal / factor))
        snafu += SNAFU_DIGITS[digit]
        decimal -= digit * factor
        factor /= BASE
    if snafu[0] == '0':
        return snafu[1:]
    return snafu


snafu_numbers = parse_input("25/input.txt")
for s in snafu_numbers:
    assert s == to_snafu(to_decimal(s))
decimals = [to_decimal(s) for s in snafu_numbers]
total_decimal = sum(decimals)
total_snafu = to_snafu(total_decimal)
print(total_snafu)


