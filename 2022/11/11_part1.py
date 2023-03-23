import parse

class Monkey:
    def __init__(self, id, items, operation, divisible_by, target_on_true, target_on_false):
        self.id = id
        self.items = items
        self.n_inspections = 0
        self.divisible_by = divisible_by
        self.target_on_true = target_on_true
        self.target_on_false = target_on_false
        self.operation = operation

    def _update_worry_level(self, old):
        new = eval(self.operation)
        # new = new // 3
        new = new % (7*19*5*11*17*13*2*3)
        return new

    def inspect_all_items(self, all_monkeys):
        for item in self.items:
            item = self._update_worry_level(item)
            if (item % self.divisible_by) == 0:
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
for _ in range(n_rounds):
    for m in monkeys:
        m.inspect_all_items(monkeys)

for m in monkeys:
    print(f"Monkey {m.id}: {m.n_inspections}")
n_inspections = sorted([m.n_inspections for m in monkeys])
print(n_inspections[-2] * n_inspections[-1])





