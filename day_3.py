with open('inputs/day_3.txt', 'r') as f:
    inputs = [row.rstrip() for row in f.readlines()]


def calculate_priority(char: str):
    if ord('a') <= ord(char) <= ord('z'):
        return 1 + (ord(char) - ord('a'))
    return 27 + (ord(char) - ord('A'))


def common_items_from_bag(elf_bag: str):
    left = set(elf_bag[:len(elf_bag) // 2])
    right = set(elf_bag[len(elf_bag) // 2:])
    return left.intersection(right)


def part_one():
    sum_prios = 0
    for elf_bag in inputs:
        common = common_items_from_bag(elf_bag)
        prio = sum([calculate_priority(item) for item in common])
        sum_prios += prio
    return sum_prios


def part_two():
    badge_prio = 0
    for i in range(0, len(inputs), 3):
        first = set(inputs[i])
        second = set(inputs[i+1])
        third = set(inputs[i+2])
        badge = first.intersection(second).intersection(third)
        badge_prio += calculate_priority(badge.pop())
    return badge_prio


print(part_one())
print(part_two())
