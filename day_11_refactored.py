import math
from functools import reduce
from typing import Callable

from day_11 import Monkey

with open('inputs/day_11.txt', 'r') as f:
    inputs = f.read()

monkeys = [Monkey.from_input(m) for m in inputs.split('\n\n')]


def monkey_business(rounds: int, relief_fn: Callable):
    monkeys = [Monkey.from_input(m) for m in inputs.split('\n\n')]
    monkey_bznz = [0] * len(monkeys)
    for _ in range(rounds):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            eval_items = [relief_fn(item) for item in monkey.eval()]
            monkey_bznz[i] += len(eval_items)
            monkey.items.clear()
            for item in eval_items:
                if item % monkey.monkey_test == 0:
                    monkeys[monkey.on_true_throw_to].items.append(item)
                else:
                    monkeys[monkey.on_false_throw_to].items.append(item)
    monkey_bznz.sort()
    return monkey_bznz[-1] * monkey_bznz[-2]


lcm = math.lcm(*[m.monkey_test for m in monkeys])
print(monkey_business(20, lambda x: x//3))
print(monkey_business(10000, lambda x: x % lcm))
