from dataclasses import dataclass
from functools import reduce
from typing import List


@dataclass
class Range:
    start: int
    end: int

    def fully_overlaps(self, other: 'Range') -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: 'Range') -> bool:
        return other.start <= self.start <= other.end


def get_inputs() -> List[List[Range]]:
    with open('inputs/day_4.txt', 'r') as f:
        inputs: List[str] = [row.rstrip() for row in f.readlines()]

    parsed_inputs = []
    for row in inputs:
        split = row.split(',')
        parsed = [section.split('-') for section in split]
        flattened = reduce(lambda l, r: l+r, parsed)
        mapped = list(map(lambda x: int(x), flattened))
        parsed_inputs.append([Range(mapped[0], mapped[1]), Range(mapped[2], mapped[3])])
    return parsed_inputs


fully_overlaps = 0
partial_overlaps = 0
for row in get_inputs():
    if row[0].fully_overlaps(row[1]) or row[1].fully_overlaps(row[0]):
        fully_overlaps += 1
    if row[0].overlaps(row[1]) or row[1].overlaps(row[0]):
        partial_overlaps += 1
print(fully_overlaps)
print(partial_overlaps)

# part_one = sum(map(lambda r: 1 if r[0].fully_intersects_with(r[1]) else 0,  get_inputs()))
# print(part_one)