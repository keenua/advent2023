from dataclasses import dataclass
from typing import List, Mapping

from part1 import find_numbers_in_the_line, read_matrix


@dataclass(frozen=True)
class Number:
    value: int
    row: int
    start: int
    end: int

    def __hash__(self):
        return hash((self.value, self.row, self.start, self.end))


def get_number_map(matrix: List[str]) -> Mapping[int, Mapping[int, Number]]:
    number_map = {}
    for row, line in enumerate(matrix):
        numbers = find_numbers_in_the_line(line)
        for number in numbers:
            value = Number(
                int(line[number[0] : number[1] + 1]), row, number[0], number[1]
            )
            for col in range(value.start, value.end + 1):
                if row not in number_map:
                    number_map[row] = {}

                number_map[row][col] = value

    return number_map


def main(file: str):
    matrix = read_matrix(file)
    number_map = get_number_map(matrix)

    total = 0

    for row, line in enumerate(matrix):
        for col, char in enumerate(line):
            if char == "*":
                # find distinct numbers around
                numbers = set()
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if r == row and c == col:
                            continue

                        if r < 0 or c < 0 or r >= len(matrix) or c >= len(matrix[r]):
                            continue

                        if matrix[r][c].isdigit():
                            numbers.add(number_map[r][c])

                if len(numbers) == 2:
                    [a, b] = list(numbers)
                    total += a.value * b.value

    print(total)


if __name__ == "__main__":
    main("day3/schema.txt")
