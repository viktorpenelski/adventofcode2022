from typing import List

from util import timed, result_printing


def from_snafu(snafu: str) -> int:
    num = 0
    for i in range(len(snafu)):
        ch = snafu[i]
        if ch == '-':
            ch = -1
        elif ch == '=':
            ch = -2
        else:
            ch = int(ch)
        exp = len(snafu) - i
        num += ch * (pow(5, exp) // 5)
    return num


def to_snafu(num: int) -> str:
    snafus = ''
    while num:
        digit = num % 5
        if 0 <= digit <= 2:
            snafus += f'{digit}'
        elif digit == 3:
            snafus += '='
            num += 2
        elif digit == 4:
            snafus += '-'
            num += 1
        num //= 5
    return snafus[::-1]


@timed
@result_printing
def solve_pt_1(inputs: List[str]):
    sums = [from_snafu(line) for line in inputs]
    return to_snafu(sum(sums))


if __name__ == '__main__':
    with open('inputs/day_25.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    solve_pt_1(lines)
