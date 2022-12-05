from collections import deque
import re

with open('inputs/day_5_test.txt', 'r') as f:
    line = f.readline()
    # one box is len 3, + space between them, without a space at the end of the line
    stacks_size = (len(line) + 1) // 4
    stacks = [deque() for _ in range(stacks_size)]

    def fill_stacks(input_line: str):
        for i in range(1, len(input_line), 4):
            if input_line[i] != ' ':
                stacks[i // 4].appendleft(input_line[i])
    while '[' in line:
        fill_stacks(line)
        line = f.readline()
    line = f.readline()
    line = f.readline()
    def parse_order(input_line: str):
        x = re.findall('\d+', input_line)
        for i in range(int(x[0])):
            fr = int(x[1]) - 1
            to = int(x[2]) - 1
            block = stacks[fr].pop()
            stacks[to].append(block)
        
    while line:
        parse_order(line)
        line = f.readline()

answer = ''
for stack in stacks:
    answer += stack.pop()
print(answer)