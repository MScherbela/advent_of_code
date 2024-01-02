#%%
import collections
import copy
import numpy as np

class Block:
    def __init__(self, ranges=None):
        if ranges is None:
             # ranges are [min, max), i.e. they include the minimum value, but not the maximum value
            ranges = {k: [1, 4001] for k in "xmas"}
        self.ranges = ranges.copy()

    def volume(self):
        return np.prod([r[1] - r[0] for r in self.ranges.values()])

    def split(self, k, t, op):
        """Return two blocks. The first corresponds to true, the second to false."""
        ranges_true = copy.deepcopy(self.ranges)
        ranges_false = copy.deepcopy(self.ranges)
        if op == '>':
            ranges_true[k][0] = t + 1
            block_true = Block(ranges_true)
            ranges_false[k][1] = t + 1
            block_false = Block(ranges_false)
        elif op == '<':
            ranges_true[k][1] = t
            block_true = Block(ranges_true)
            ranges_false[k][0] = t
            block_false = Block(ranges_false)
        block_true = block_true if block_true.volume() > 0 else None
        block_false = block_false if block_false.volume() > 0 else None
        return block_true, block_false

    def key(self):
        return tuple([tuple(self.ranges[k]) for k in "xmas"])

    def __str__(self):
        s = ""
        for k in "xmas":
            s += f"{k}: {self.ranges[k][0]}-{self.ranges[k][1]}, "
        s += f"V: {self.volume()}"
        return s

    def __repr__(self):
        return "<Block " + str(self) + ">"

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

    def __call__(self, block: Block):
        outputs = []
        for k, op, t, target in zip(self.keys, self.operations, self.thresholds, self.targets):
            b_t, block = block.split(k, t, op)
            if b_t is not None:
                outputs.append((b_t, target))
            if block is None:
                break
        if block is not None:
            outputs.append((block, self.fallback))
        return outputs


            

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

rules, _ = parse_input("/home/mscherbela/develop/advent_of_code/2023/19/input.txt")

# Apply all rules
blocks = [(Block(), "in")]
accepted_blocks = {}
ind_round = 0
while blocks:
    new_blocks = []
    for b, rule in blocks:
        if rule == "A":
            accepted_blocks[b.key()] = b
            continue
        elif rule == "R":
            continue
        else:
            new_blocks += rules[rule](b)
    blocks = new_blocks
    ind_round += 1
blocks = accepted_blocks

V_total = 0
for b in blocks.values():
    V_total += b.volume()
print(V_total)

            






            