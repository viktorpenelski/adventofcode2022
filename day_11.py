from dataclasses import dataclass
from functools import reduce
from typing import List

with open('inputs/day_11.txt', 'r') as f:
    inputs = f.read()


@dataclass
class Monkey:
    starting_items: List[int]
    operation: str
    test_divisible_by: int
    on_true_throw_to: int
    on_false_throw_to: int

    trues: int = 0
    falses: int = 0

    def eval(self):
        return [eval(f'{item} {self.operation}') for item in self.starting_items]

    @staticmethod
    def from_input(lines: str) -> 'Monkey':
        rows = lines.split('\n')
        starting_items = None
        operation = None
        test_divisible_by = None
        on_true_throw_to = None
        on_false_throw_to = None
        for row in rows:
            row = row.strip()
            if row.startswith('Monkey'):
                pass
            if row.startswith('Starting items:'):
                starting_items = row.replace(',', '').split(' ')[2:]
                starting_items = [int(item) for item in starting_items]
            if row.startswith('Operation:'):
                operation = row.split('Operation: new = old ')[1]
                if operation == '* old':
                    operation = '** 2'
            if row.startswith('Test: divisible by '):
                test_divisible_by = int(row.split('Test: divisible by ')[1])
            if row.startswith('If true: throw to monkey '):
                on_true_throw_to = int(row.split('If true: throw to monkey ')[1])
            if row.startswith('If false: throw to monkey '):
                on_false_throw_to = int(row.split('If false: throw to monkey ')[1])
        return Monkey(
            starting_items=starting_items,
            operation=operation,
            test_divisible_by=test_divisible_by,
            on_true_throw_to=on_true_throw_to,
            on_false_throw_to=on_false_throw_to
        )


monkeys = [Monkey.from_input(m) for m in inputs.split('\n\n')]
monkey_bznz = [0] * len(monkeys)
worry_treshhold = reduce(lambda x, y: x * y, [m.test_divisible_by for m in monkeys])
round = 0
for _ in range(10000):
    print(f'round: {_}')
    print(monkey_bznz)
    for i in range(len(monkeys)):
        monkey = monkeys[i]
        eval_items = monkey.eval()
        eval_items = [item % worry_treshhold for item in eval_items]
        # eval_items = [item//3 for item in eval_items]

        monkey_bznz[i] += len(eval_items)
        monkey.starting_items = []
        for item in eval_items:
            if item % monkey.test_divisible_by == 0:
                monkey.trues += 1
                monkeys[monkey.on_true_throw_to].starting_items.append(item)
            else:
                monkey.falses += 1
                monkeys[monkey.on_false_throw_to].starting_items.append(item)
monkey_bznz.sort()
print(monkey_bznz[-1] * monkey_bznz[-2])
