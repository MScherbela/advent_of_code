import parse

class Item:
    def __init__(self, worry):
        self.initial_worry = worry
        self.operations = []
        self.remainder_cache = {}

    def divisible_by(self, n):
        if n not in self.remainder_cache:
            self.remainder_cache[n] = (self.initial_worry % n, 0)
        remainder, initial_op = self.remainder_cache[n]
        for op, data in self.operations[initial_op:]:
            if op == "square":
                remainder = remainder**2
            elif op == "+":
                remainder = remainder + data
            elif op == "*":
                remainder = remainder * data
            remainder = remainder % n
        self.remainder_cache[n] = (remainder, len(self.operations))
        return (remainder % n) == 0

    def apply_operation(self, operation):
        if operation == "old * old":
            self.operations.append(('square', None))
        elif "*" in operation:
            self.operations.append(("*", int(operation.split("* ")[1])))
        elif "+" in operation:
            self.operations.append(("+", int(operation.split("+ ")[1])))
        else:
            raise ValueError("Unknown operation")


class Monkey:
    def __init__(self, id, items, operation, divisible_by, target_on_true, target_on_false):
        self.id = id
        self.items = [Item(x) for x in items]
        self.n_inspections = 0
        self.divisible_by = divisible_by
        self.target_on_true = target_on_true
        self.target_on_false = target_on_false
        self.operation = operation

    def inspect_all_items(self, all_monkeys):
        for item in self.items:
            item.apply_operation(self.operation)
            if item.divisible_by(self.divisible_by):
                target = self.target_on_true
            else:
                target = self.target_on_false
            all_monkeys[target].items.append(item)
            self.n_inspections += 1
        self.items = []

    @classmethod
    def from_input(cls, input):
        template = """Monkey {id:d}:
  Starting items: {items}
  Operation: new = {operation}
  Test: divisible by {divisible_by:d}
    If true: throw to monkey {target_on_true:d}
    If false: throw to monkey {target_on_false:d}"""

        data = parse.parse(template, input).named
        return cls(data['id'],
                   [int(x) for x in data['items'].split(",")],
                   data['operation'],
                   data['divisible_by'],
                   data['target_on_true'],
                   data['target_on_false'])


with open("11/input.txt") as f:
    data = f.read().split("\n\n")
    monkeys = [Monkey.from_input(d) for d in data]


n_rounds = 10_000
for ind_round in range(n_rounds):
    if (ind_round % 50) == 0:
        print(ind_round)
    for m in monkeys:
        m.inspect_all_items(monkeys)

for m in monkeys:
    print(f"Monkey {m.id}: {m.n_inspections}")
n_inspections = sorted([m.n_inspections for m in monkeys])
print(n_inspections[-2] * n_inspections[-1])

