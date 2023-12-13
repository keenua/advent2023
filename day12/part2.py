from functools import lru_cache
from typing import Tuple
from part1 import ROW, read_file


TUPLE_ROW = Tuple[str, Tuple[int, ...]]


@lru_cache(maxsize=None)
def get_combs(row: TUPLE_ROW) -> int:
    data, sizes = row

    count = 0
    if not sizes:
        return 0 if "#" in data else 1

    size = sizes[0]

    if len(data) < size:
        return 0

    if "." not in data[:size]:
        if len(data) == size or data[size] != "#":
            rest = data[size + 1 :]
            rest_sizes = sizes[1:]
            count += get_combs((rest, rest_sizes))

    if data[0] != "#":
        count += get_combs((data[1:], sizes))
    return count


def expand(row: ROW) -> TUPLE_ROW:
    data, sizes = row

    new_data = "?".join([data] * 5)
    new_sizes = sizes * 5
    return (new_data, tuple(new_sizes))


def main(file: str):
    rows = read_file(file)
    rows = [expand(row) for row in rows]

    result = 0
    for index, row in enumerate(rows):
        print(f"Row {index} / {len(rows)}")
        combs = get_combs(row)
        print(combs)
        result += combs

    print(result)


if __name__ == "__main__":
    main("day12/springs.txt")
