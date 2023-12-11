from typing import List, Tuple
import numpy as np


def read_file(file: str) -> np.ndarray:
    with open(file, "r") as f:
        lines = f.readlines()

        arr = np.empty((len(lines), len(lines[0].strip())), dtype=bool)

        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                arr[i][j] = char == "#"

    return arr


def get_expansion(arr: np.ndarray) -> Tuple[List[int], List[int]]:
    rows_to_expand = []
    for i, row in enumerate(arr):
        if not np.any(row):
            rows_to_expand.append(i)

    cols_to_expand = []
    for i, col in enumerate(arr.T):
        if not np.any(col):
            cols_to_expand.append(i)

    return rows_to_expand, cols_to_expand


def expand(arr: np.ndarray) -> np.ndarray:
    rows_to_expand, cols_to_expand = get_expansion(arr)

    shift = 0
    for i in rows_to_expand:
        arr = np.insert(arr, i + shift, False, axis=0)
        shift += 1

    shift = 0
    for i in cols_to_expand:
        arr = np.insert(arr, i + shift, False, axis=1)
        shift += 1

    return arr


def print_image(arr: np.ndarray):
    for row in arr:
        for col in row:
            print("#" if col else ".", end="")
        print()
    print()


def get_points(arr: np.ndarray) -> List[Tuple[int, int]]:
    points = []
    for i, row in enumerate(arr):
        for j, col in enumerate(row):
            if col:
                points.append((i, j))
    return points


def get_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_all_distances(points: List[Tuple[int, int]]) -> List[int]:
    result = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            result.append(get_distance(points[i], points[j]))

    return result


def main(file: str):
    image = read_file(file)
    image = expand(image)
    print_image(image)

    points = get_points(image)
    distances = get_all_distances(points)

    print(sum(distances))


if __name__ == "__main__":
    main("day11/map.txt")
