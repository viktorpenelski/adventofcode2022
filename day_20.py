from typing import List

from util import timed, result_printing


def mix(nums: List[int], iterations: int) -> List[int]:
    idxs = list(range(len(nums)))
    for _ in range(iterations):
        for i in range(len(nums)):
            i_idx = idxs.index(i)
            idxs.pop(i_idx)
            insert_before_idx = (i_idx + nums[i]) % len(idxs)
            idxs.insert(insert_before_idx, i)
    return [nums[idxs[i]] for i in range(len(idxs))]


@timed
@result_printing
def solve_pt_1(nums: List[int]) -> int:
    nums = mix(nums, 1)
    zero = nums.index(0)
    return sum(nums[(zero + i) % len(nums)] for i in [1000, 2000, 3000])


@timed
@result_printing
def solve_pt_2(nums: List[int]) -> int:
    nums = mix([int(x) * 811589153 for x in nums], 10)
    zero = nums.index(0)
    return sum(nums[(zero + i) % len(nums)] for i in [1000, 2000, 3000])


if __name__ == '__main__':
    with open('inputs/day_20.txt', 'r') as f:
        inputs = [int(line) for line in f.readlines()]
    solve_pt_1(inputs)
    solve_pt_2(inputs)


