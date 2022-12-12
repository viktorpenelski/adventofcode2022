from dataclasses import dataclass
from functools import reduce
from typing import List

with open('inputs/day_11.txt', 'r') as f:
    inputs = f.read()


@dataclass
class Monkey:
    items: List[int]
    operation: str
    monkey_test: int
    on_true_throw_to: int
    on_false_throw_to: int

    def eval(self):
        return [eval(f'{item} {self.operation}') for item in self.items]

    @staticmethod
    def from_input(lines: str) -> 'Monkey':
        rows = lines.split('\n')
        for row in rows:
            row = row.strip()
            if row.startswith('Monkey'):
                pass
            if row.startswith('Starting items:'):
                starting_items = row.replace(',', '').split(' ')[2:]
                starting_items = [int(item) for item in starting_items]
            if row.startswith('Operation:'):
                operation = row.split('Operation: new = old ')[1].replace('* old', '** 2')
            if row.startswith('Test: divisible by '):
                test_divisible_by = int(row.split('Test: divisible by ')[1])
            if row.startswith('If true: throw to monkey '):
                on_true_throw_to = int(row.split('If true: throw to monkey ')[1])
            if row.startswith('If false: throw to monkey '):
                on_false_throw_to = int(row.split('If false: throw to monkey ')[1])
        return Monkey(
            items=starting_items,
            operation=operation,
            monkey_test=test_divisible_by,
            on_true_throw_to=on_true_throw_to,
            on_false_throw_to=on_false_throw_to
        )


def solve():
    monkeys = [Monkey.from_input(m) for m in inputs.split('\n\n')]
    monkey_bznz = [0] * len(monkeys)
    worry_treshhold = reduce(lambda x, y: x * y, [m.monkey_test for m in monkeys])
    for _ in range(10000):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            eval_items = monkey.eval()
            eval_items = [item % worry_treshhold for item in eval_items]
            # eval_items = [item//3 for item in eval_items]

            monkey_bznz[i] += len(eval_items)
            monkey.items = []
            for item in eval_items:
                if item % monkey.monkey_test == 0:
                    monkeys[monkey.on_true_throw_to].items.append(item)
                else:
                    monkeys[monkey.on_false_throw_to].items.append(item)
    monkey_bznz.sort()
    print(monkey_bznz[-1] * monkey_bznz[-2])

#solve()