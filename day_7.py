from collections import deque
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Optional, Set
from functools import cache, cached_property

with open('inputs/day_7.txt', 'r') as f:
    input_lines = f.readlines()

with open('inputs/day_7_test.txt', 'r') as f:
    test_lines = f.readlines()


MAX_SIZE = 100000
TOTAL_SPACE = 70000000
MIN_UNUSED = 30000000

def parse_input(input_l):
    return input_l

@dataclass
class DirNode:
    name: str
    children: Set['DirNode'] = field(default_factory=set)
    parent: Optional['DirNode'] = None
    own_size: int = 0

    @cache
    def calculate_total_size(self):
        return self.own_size + sum([child.calculate_total_size() for child in self.children])

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other.name


def solve_one(input_l: List[str]):
    dirs_map = {}
    dir_path = deque()
    for line in input_l:
        if line.startswith('$'):
            if 'cd' in line:
                dir_name = line.rstrip().split()[2]
                if dir_name == '..':
                    dir_path.pop()
                else:
                    parent_path = dir_path[-1].name if len(dir_path) > 0 else ''
                    full_path = parent_path + dir_name
                    dir_node = dirs_map.get(full_path, DirNode(full_path))
                    dir_path.append(dir_node)
                    dir_node.parent = dirs_map.get(parent_path)
                    if dir_node.parent is not None:
                        dir_node.parent.children.add(dir_node)
                    dirs_map[full_path] = dir_node
            if 'ls' in line:
                pass
        else:
            if line.startswith('dir'):
                continue
            size = int(line.split(' ')[0])
            dir_node = dirs_map.get(dir_path[-1].name)
            assert dir_node is not None
            dir_node.own_size += size

    dirs_with_size = {d.name: d.calculate_total_size() for d in list(dirs_map.values())}
    sum_of_dirs_smaller_than_max_size = sum([size for size in dirs_with_size.values() if size <= MAX_SIZE])
    print(sum_of_dirs_smaller_than_max_size)
    space_available = TOTAL_SPACE - dirs_map['/'].calculate_total_size()
    space_required = MIN_UNUSED - space_available
    dirs_with_enough_space = [size for size in dirs_with_size.values() if size >= space_required]
    dirs_with_enough_space.sort()
    print(dirs_with_enough_space[0])


solve_one(test_lines)
solve_one(input_lines)