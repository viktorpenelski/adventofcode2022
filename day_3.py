inputs = []
with open('inputs/day_3.txt', 'r') as f:
    inputs = [row.rstrip() for row in f.readlines()]
    for row in f.readlines():
        inputs = [r.r]
        rstrip = row.rstrip()


def calculate_priority(char: str):
    if ord('a') <= ord(char) <= ord('z'):
        return 1 + (ord(char) - ord('a'))
    return 27 + (ord(char) - ord('A'))

def part_one():
    sum_prios = 0
    for elf_bag in inputs:
        prio = 0
        left = set(elf_bag[0:len(elf_bag)//2])
        right = set(elf_bag[len(elf_bag)//2:len(elf_bag)])
        common = left.intersection(right)
        for item in common:
            prio += calculate_priority(item)
        sum_prios += prio
    return sum_prios

# badge_prio = 0
# for i in range(0, len(inputs), 3):
#     first = set(inputs[i][0] + inputs[i][1])
#     second = set(inputs[i+1][0] + inputs[i+1][1])
#     third = set(inputs[i+2][0] + inputs[i+2][1])
#     badge = first.intersection(second).intersection(third)
#     badge_prio += calculate_priority(badge.pop())


print(part_one())