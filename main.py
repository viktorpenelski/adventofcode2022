import os

from aocd import get_data


def download_year(year: int, overwrite: bool = False):
    for day in range(1, 26):
        file_name = f'inputs/day_{day}.txt'
        if os.path.exists(file_name) and not overwrite:
            continue
        data = get_data(year=year, day=day)
        with open(file_name, 'w') as f:
            f.write(data)


if __name__ == '__main__':
    download_year(2022, True)