from typing import List, Tuple


def read_matrix(file: str) -> List[str]:
    with open(file) as f:
        return [line.strip() for line in f.read().splitlines()]


def find_numbers_in_the_line(line: str) -> List[Tuple[int, int]]:
    """
    Returns list of tuples (start_index, end_index)
    """
    numbers = []
    i = 0
    while i < len(line):
        if line[i].isdigit():
            start_index = i
            i += 1
            while i < len(line) and line[i].isdigit():
                i += 1

            numbers.append((start_index, i - 1))
        else:
            i += 1
    return numbers


def has_symbol_around(row: int, pos: Tuple[int, int], matrix: List[str]) -> bool:
    for r in range(row - 1, row + 2):
        for c in range(pos[0] - 1, pos[1] + 2):
            if r == row and c == pos[0]:
                continue

            if r < 0 or c < 0 or r >= len(matrix) or c >= len(matrix[r]):
                continue

            char = matrix[r][c]
            if not char.isdigit() and char != ".":
                return True

    return False


def main(file: str):
    matrix = read_matrix(file)
    total = 0
    for row, line in enumerate(matrix):
        numbers = find_numbers_in_the_line(line)
        for number in numbers:
            if has_symbol_around(row, number, matrix):
                value = int(line[number[0]: number[1] + 1])
                total += value

    print(total)


if __name__ == "__main__":
    main("day3/schema.txt")
