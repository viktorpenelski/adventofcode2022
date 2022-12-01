with open('inputs/day_1.txt', 'r') as f:
    elf_cals_input = [line.rstrip('\n') for line in f.readlines()]

elf_cals = []
current_elf_cals = 0
for row in elf_cals_input:
    try:
        current_elf_cals += int(row)
    except ValueError:
        elf_cals.append(current_elf_cals)
        current_elf_cals = 0
elf_cals.append(current_elf_cals)

print(max(elf_cals))

elf_cals.sort()
print(sum(elf_cals[-3:]))
