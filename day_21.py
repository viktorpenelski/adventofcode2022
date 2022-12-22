import operator
from typing import Dict

op_lookup = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


class Monkey:
    name: str
    noises: str
    _all_monkeys: Dict[str, 'Monkey'] = {}

    def __init__(self, name: str, noises: str):
        self.name = name
        self.noises = noises
        Monkey._all_monkeys[name] = self

    def yell(self):
        try:
            return int(self.noises)
        except ValueError:
            first_monkey, op, second_money = self.noises.split(' ')
            return op_lookup[op](Monkey._all_monkeys[first_monkey].yell(), Monkey._all_monkeys[second_money].yell())


if __name__ == '__main__':
    with open('inputs/day_21.txt', 'r') as f:
        monkeys = [Monkey(line.split(':')[0].strip(), line.split(':')[1].strip()) for line in f.readlines()]
    root_monkey = Monkey._all_monkeys.pop('root')
    print(root_monkey.yell())

    root_noises = root_monkey.noises
    m1_name, _, m2_name = root_noises.split(' ')
    first_monkey = Monkey._all_monkeys[m1_name]
    second_monkey = Monkey._all_monkeys[m2_name]
    human_monkey = Monkey._all_monkeys['humn']
    noise = 1
    human_monkey.noises = noise
    equality = first_monkey.yell() - second_monkey.yell()
    new_equality = equality
    while abs(new_equality) <= abs(equality):
        noise = human_monkey.noises
        human_monkey.noises = noise * 2
        new_equality = first_monkey.yell() - second_monkey.yell()

    equality = new_equality
    start = noise//2
    end = noise
    while start <= end:
        mid = start + (end - start) // 2
        human_monkey.noises = mid
        new_equality = first_monkey.yell() - second_monkey.yell()
        if new_equality == 0:
            break
        if new_equality < 0 and equality < 0:
            lc = abs(new_equality)
            rc = abs(equality)
        else:
            lc = new_equality
            rc = equality
        if lc < rc:
            end = mid - 1
        else:
            start = mid + 1
    noises = human_monkey.noises
    print(human_monkey.noises)