# A rock B paper C scis
# X     Y           Z
# 1 2 3 - shape
# 0 3 6 l/w/d

inputs = []
with open('inputs/day_2.txt', 'r') as f:
    for row in f.readlines():
        inputs.append(row.rstrip().split(' '))

total_score = 0
for inp in inputs:
    round_score = 0
    result = (ord(inp[1]) - ord('X')) - (ord(inp[0]) - ord('A'))
    if result == 0:
        round_score += 3
    elif result == 1 or result == -2:
        round_score += 6

    round_score += ord(inp[1]) - ord('X') + 1
    total_score += round_score

print(total_score)


total_score = 0
for inp in inputs:
    result = 0  # (ord(inp[1]) - ord('X')) - (ord(inp[0]) - ord('A'))
    if inp[1] == 'Y':
        result += 3
        result += (ord(inp[0]) - ord('A')) + 1
    elif inp[1] == 'Z':
        result += 6
        result += ((ord(inp[0]) - ord('A')) + 1) % 3 + 1
    elif inp[1] == 'X':
        if inp[0] == 'A':
            result += 3
        else:
            result += (ord(inp[0]) - ord('A') - 1) + 1

    print(result)
    total_score += result

print(total_score)