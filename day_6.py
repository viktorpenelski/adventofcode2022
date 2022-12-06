with open('inputs/day_6.txt', 'r') as f:
    packet = f.readline()


def count_chars(target_unique: int) -> int:
    for i in range(target_unique, len(packet)):
        window = packet[i-target_unique: i]
        if len(set(window)) == target_unique:
            return i


print(count_chars(4))
print(count_chars(14))
