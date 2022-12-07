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

def parse_input(input_l):
    return input_l

@dataclass
class DirNode:
    name: str
    children: Set['DirNode'] = field(default_factory=set)
    parent: Optional['DirNode'] = None
    own_size: int = 0

    @cache
    def parents_path(self):
        if not self.parent:
            return self.name
        return self.parent.parents_path() + '/' + self.name

    @cache
    def calculate_total_size(self):
        return self.own_size + sum([child.calculate_total_size() for child in self.children])

    def __hash__(self):
        return self.parents_path().__hash__()

    def __eq__(self, other):
        return self.parents_path() == other.parents_path()



def solve_one(input_l: str):
    dirs_map = {}
    dir_path = deque()
    current_dir_name = None
    for line in input_l:
        if line.startswith('$'):
            if 'cd' in line:
                dir = line.rstrip().split()[2]
                if dir == '..':
                    dir_path.pop()
                    current_dir_name = dir_path[-1].name
                else:
                    dir_node = dirs_map.get(dir, DirNode(dir))
                    dir_path.append(dir_node)
                    dir_node.parent = dirs_map.get(current_dir_name)
                    if dir_node.parent is not None:
                        dir_node.parent.children.add(dir_node)
                    dirs_map[dir] = dir_node
                    current_dir_name = dir
            if 'ls' in line:
                pass
        else:
            if line.startswith('dir'):
                continue
            size = int(line.split(' ')[0])
            dir_node = dirs_map.get(current_dir_name)
            assert dir_node is not None
            dir_node.own_size += size

    dirs_with_size = {d.name: d.calculate_total_size() for d in list(dirs_map.values())}
    return sum([size for size in dirs_with_size.values() if size <= MAX_SIZE])

def solve_two(input_l: str):

    return input_l


#print(f'One test: {solve_one(parse_input(test_lines))}')
print(f'One real: {solve_one(parse_input(input_lines))}')
#print(f'Two test: {solve_two(parse_input(test_lines))}')
#print(f'Two real: {solve_two(parse_input(input_lines))}')