from collections import defaultdict


class BaseOp:
    def __init__(self):
        self.cycles_left = self.get_cycle_count()

    def get_cycle_count(self) -> int:
        raise NotImplementedError()

    def apply(self, register: int):
        self.cycles_left -= 1
        if self.cycles_left > 0:
            return register
        return self._apply(register)

    def _apply(self, register: int):
        raise NotImplementedError()


class NoOp(BaseOp):
    def get_cycle_count(self) -> int:
        return 1

    def _apply(self, register: int):
        return register


class AddXOp(BaseOp):
    def __init__(self, arguments: str):
        super(AddXOp, self).__init__()
        self.x = int(arguments)

    def get_cycle_count(self) -> int:
        return 2

    def _apply(self, register: int):
        return register + self.x


with open('inputs/day_10.txt', 'r') as f:
    inputs = [l.strip() for l in f.readlines()]

delayed_ops = []
x = 1
target_cycle = 20
cycle_gap = 40
signal_strength = 0
cycle = 1
index = 0

image = [['.'] * 40 for _ in range(6)]

def read_instruction(idx: int):
    row = inputs[idx]
    if row.startswith('noop'):
        return NoOp()
    if row.startswith('addx'):
        addx_cmd, arguments = row.rsplit(' ', 1)
        return AddXOp(arguments)
    raise Exception(f'unknown operation {row}')


while index < len(inputs):
    sprite_idx = cycle - 1
    sprite_row = sprite_idx // 40
    sprite_col = sprite_idx % 40
    if abs(x - sprite_col) <= 1:
        image[sprite_row][sprite_col] = '#'
    if len(delayed_ops) == 0:
        op = read_instruction(index)
        delayed_ops.append(op)
        index += 1
    if cycle == target_cycle:
        print(f'x: {x}, cycle = {cycle}, product = {target_cycle * x}')
        signal_strength += target_cycle * x
        target_cycle += cycle_gap
    for op in delayed_ops:
        x = op.apply(x)
    delayed_ops = [op for op in delayed_ops if op.cycles_left > 0]
    cycle += 1

print(signal_strength)
for r in image:
    print(''.join(r))