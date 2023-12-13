from typing import List, Optional, Tuple
from colorama import Back


ROWS = List[str]
COLS = List[str]
PATTERN = Tuple[ROWS, COLS]


def get_cols(rows: List[str]) -> List[str]:
    cols: List[str] = []

    for row in rows:
        for index, char in enumerate(row):
            if len(cols) <= index:
                cols.append("")

            cols[index] += char

    return cols


def read_file(file: str) -> List[PATTERN]:
    result: List[PATTERN] = []

    rows: List[str] = []

    with open(file) as f:
        for line in f.readlines():
            line = line.strip()

            if not line:
                cols = get_cols(rows)
                result.append((rows, cols))
                rows = []
                continue

            rows.append(line)

    cols = get_cols(rows)
    result.append((rows, cols))
    return result


def print_pattern(pattern: PATTERN, highlight: Optional[Tuple[int, int]] = None, row_mirror: int = -1, col_mirror: int = -1):
    rows, _ = pattern
    y, x = highlight if highlight else (-1, -1)

    for r, row in enumerate(rows):
        for c, col in enumerate(row):
            if r == y and c == x:
                print(Back.GREEN + col, end="")
                print(Back.RESET, end="")
            else:
                print(col, end="")

            if col_mirror > 0 and c == col_mirror - 1:
                print("|", end="")

        print()
            
        if row_mirror > 0 and r == row_mirror - 1:
            length = len(row) + (1 if col_mirror > 0 else 0)
            print("-" * length)
            


def get_repeats(lines: List[str]) -> List[int]:
    result = []
    for i in range(len(lines) - 1):
        if lines[i] == lines[i + 1]:
            result.append(i)
    return result


def validate_mirror(lines: List[str], index: int) -> bool:
    for i in range(index + 1):
        left = lines[index - i]

        if index + i + 1 >= len(lines):
            break

        right = lines[index + i + 1]

        if left != right:
            return False

    return True


def get_mirrors(lines: List[str]) -> List[int]:
    repeats = get_repeats(lines)

    mirrors = [index + 1 for index in repeats if validate_mirror(lines, index)]
    return mirrors


def main(file: str):
    result = 0

    for rows, cols in read_file(file):
        col_mirrors = get_mirrors(cols)
        row_mirrors = get_mirrors(rows)

        col_mir = max(col_mirrors) if col_mirrors else 0
        row_mir = max(row_mirrors) if row_mirrors else 0

        result += col_mir + 100 * row_mir

    print(result)


if __name__ == "__main__":
    main("day13/mirrors.txt")
