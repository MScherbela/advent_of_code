import enum
import dataclasses
import numpy as np

class InstructionType(enum.Enum):
    NOOP = enum.auto()
    ADDX = enum.auto()

@dataclasses.dataclass
class Instruction:
    instruction_type: InstructionType
    data: int | None = None

instructions = []
with open("10/input.txt") as f:
    for line in f:
        tokens = line.strip().split(" ")
        if tokens[0] == "noop":
            instructions.append(Instruction(InstructionType.NOOP))
        elif tokens[0] == "addx":
            instructions.append(Instruction(InstructionType.ADDX, int(tokens[1])))

register_changes = [[0]]
for ins in instructions:
    if ins.instruction_type == InstructionType.NOOP:
        register_changes.append(np.zeros(1, int))
    elif ins.instruction_type == InstructionType.ADDX:
        register_changes.append(np.array([0, ins.data], int))
register_changes = np.concatenate(register_changes)

register_value = 1 + np.cumsum(register_changes)
signal_strength = 0
for cycle_nr in 20 + np.arange(6) * 40:
    signal_strength += cycle_nr * register_value[cycle_nr - 1]
print(signal_strength)

output = ""
line_width = 40
for i, v in enumerate(register_value):
    x = i % line_width
    if v - 1 <= x <= v+1:
        output += "#"
    else:
        output += " "
    if ((i+1)%40) == 0:
        output += "\n"
print(output)




