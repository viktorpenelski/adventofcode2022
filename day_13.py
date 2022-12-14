import functools
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Dict

with open('inputs/test_day_13.txt', 'r') as f:
    test_lines = [l.strip() for l in f.readlines()]

with open('inputs/day_13.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]


def compare_order(left, right):
    if type(left) is int and type(right) is int:
        if left > right:
            return -1
        if left < right:
            return 1
        return 0
    if type(left) is int:
        left = [left]
    if type(right) is int:
        right = [right]
    for li in range(len(left)):
        if li >= len(right):
            return -1
        order = compare_order(left[li], right[li])
        if order != 0:
            return order
    return len(left) < len(right)


def solve(inputs):
    pair_idx_sum = 0
    for i in range(0, len(inputs), 3):
        left = eval(inputs[i])
        right = eval(inputs[i+1])
        pair_idx = (i+3)//3
        order = compare_order(left, right)
        if order == 1:
            pair_idx_sum += pair_idx
        print(f'{pair_idx}: {order} | {pair_idx_sum}')
    return pair_idx_sum


def solve_pt2(inputs):
    items = [eval(inp) for inp in inputs if inp]
    items.append([[2]])
    items.append([[6]])
    items.sort(key=functools.cmp_to_key(lambda x,y: -compare_order(x, y)))
    idx_first_divider = items.index([[2]]) + 1
    idx_second_divider = items.index([[6]]) + 1
    return idx_first_divider * idx_second_divider


print(solve(test_lines))
print(solve_pt2(lines))
