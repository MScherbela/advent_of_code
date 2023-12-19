#%%
with open("input.txt") as f:
    tokens = f.readline().strip().split(",")

def holiday_hash(s):
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value = value % 256
    return value

def parse_instruction(token):
    if token[-1] == '-':
        label = token[:-1]
        return ('-', holiday_hash(label), label)
    else:
        label, value = token.split("=")
        return ("=", holiday_hash(label), label, int(value))
    
class Box:
    def __init__(self, box_nr):
        self.box_nr = box_nr

        # maps label -> [pos, value]
        self.lenses = {} 
    
    def add_lens(self, label, value):
        existing_lens = self.lenses.get(label)
        pos = existing_lens[0] if existing_lens else len(self.lenses)
        self.lenses[label] = [pos, value]

    def remove_lens(self, label):
        existing_lens = self.lenses.get(label)
        if existing_lens:
            pos = existing_lens[0]
            del self.lenses[label]
            for l in self.lenses.values():
                if l[0] > pos:
                    l[0] -= 1

    def get_focusing_power(self):
        power = 0
        for pos, value in self.lenses.values():
            power += (1+self.box_nr) * (pos + 1) * value
        return power
    
    def __len__(self):
        return len(self.lenses)
            
instructions = [parse_instruction(t) for t in tokens]
boxes = [Box(i) for i in range(256)]

total_part1 = 0
for token in tokens:
    total_part1 += holiday_hash(token)
print("Part 1: ", total_part1)


for ins in instructions:
    ins_type, box_nr = ins[:2]
    if ins_type == "-":
        boxes[box_nr].remove_lens(ins[2])
    elif ins_type == "=":
        boxes[box_nr].add_lens(ins[2], ins[3])
    else:
        raise ValueError("Invalid instruction type")
    
    # for ind_b, b in enumerate(boxes):
    #     if len(b):
    #         print(f"Box {ind_b:3d}: {b.lenses}")
    # print("="*20)

total_part2 = 0
for b in boxes:
    total_part2 += b.get_focusing_power()
print("Part 2: ", total_part2)