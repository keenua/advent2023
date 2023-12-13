from typing import List
from part1 import PATTERN, get_mirrors, print_pattern, read_file
import os
clear = lambda: os.system('cls')


def smudge(pattern: PATTERN, row: int, col: int) -> PATTERN:
    rows, cols = pattern

    new_rows = rows.copy()
    new_cols = cols.copy()

    item = rows[row][col]

    replace = "." if item == "#" else "#"

    new_rows[row] = rows[row][:col] + replace + rows[row][col + 1 :]
    new_cols[col] = cols[col][:row] + replace + cols[col][row + 1 :]

    return (new_rows, new_cols)


def first_not(numbers: List[int], exception: int) -> List[int]:
    for number in numbers:
        if number != exception:
            return number
    return 0

def max_or_zero(numbers: List[int]) -> int:
    if numbers:
        return max(numbers)
    return 0

def process(pattern: PATTERN) -> int:
    rows, cols = pattern

    row_mirrors = get_mirrors(rows)
    col_mirrors = get_mirrors(cols)

    row_mir = max_or_zero(row_mirrors)
    col_mir = max_or_zero(col_mirrors)

    clear()
    print("ORIGINAL")
    print()
    print_pattern(pattern, row_mirror=row_mir, col_mirror=col_mir)
    print()

    max_row = 0
    max_col = 0

    for ri, _ in enumerate(rows):
        for ci, _ in enumerate(cols):
            nrows, ncols = smudge((rows, cols), ri, ci)

            ncol_mir = first_not(get_mirrors(ncols), col_mir)
            nrow_mir = first_not(get_mirrors(nrows), row_mir)

            if nrow_mir != 0 or ncol_mir != 0:
                print()
                print_pattern((nrows, ncols), (ri, ci), nrow_mir, ncol_mir)
                print()

                if ncol_mir == 0:
                    max_row = max(nrow_mir, max_row)
                elif nrow_mir == 0:
                    max_col = max(ncol_mir, max_col)
                elif ncol_mir < nrow_mir:
                    max_col = max(ncol_mir, max_col)
                else:
                    max_row = max(nrow_mir, max_row)
                break

    if max_row == 0:
        return max_col

    if max_col == 0:
        return 100 * max_row

    if max_row < max_col:
        return 100 * max_row

    return max_col


def main(file: str):
    result = 0

    for pattern in read_file(file):
        res = process(pattern)
        print(res)
        result += res

        # input()

    print(result)


if __name__ == "__main__":
    main("day13/mirrors.txt")
