#%%
import collections

class Rule:
    def __init__(self, rule_str):
        self.keys = []
        self.operations = []
        self.thresholds = []
        self.targets = []
        self.fallback = None

        rule_str = rule_str.split(',')
        for token in rule_str:
            if '>' in token:
                k, t = token.split('>')
                t, target = t.split(':')
                t = int(t)
                op = '>'
            elif '<' in token:
                k, t = token.split('<')
                t, target = t.split(':')
                t = int(t)
                op = '<'
            else:
                self.fallback = token
                break
            self.keys.append(k)
            self.operations.append(op)
            self.thresholds.append(t)
            self.targets.append(target)

    def __call__(self, data):
        for k, op, t, target in zip(self.keys, self.operations, self.thresholds, self.targets):
            if op == '>':
                if data[k] > t:
                    return target
            elif op == '<':
                if data[k] < t:
                    return target
        return self.fallback

def parse_input(fname):
    is_rule = True
    rules = {}
    items = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                is_rule = False
                continue
            if is_rule:
                rule_name, rule_str = line.split('{')
                rules[rule_name] = Rule(rule_str[:-1])
            else:
                line = line[1:-1]
                substrings = line.split(',')
                item = {}
                for s in substrings:
                    k, v = s.split('=')
                    item[k] = int(v)
                items.append(item)
    return rules, items

rules, items = parse_input("/home/mscherbela/develop/advent_of_code/2023/19/input.txt")

total_part1 = 0
for item in items:
    r = "in"
    while (r != "A") and (r != "R"):
        r = rules[r](item)
    if r == "A":
        total_part1 += item["x"] + item["m"] + item["a"] + item["s"]
print("Part 1: ", total_part1)


            