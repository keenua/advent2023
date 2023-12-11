from typing import List, Tuple
from part1 import get_all_distances, get_expansion, read_file, get_points


def expand_point(
    point: Tuple[int, int], rows: List[int], cols: List[int], mult: int = 1000000
) -> Tuple[int, int]:
    rows_to_add = sum([1 for row in rows if point[0] > row])
    point = (point[0] + rows_to_add * (mult - 1), point[1])

    cols_to_add = sum([1 for col in cols if point[1] > col])
    point = (point[0], point[1] + cols_to_add * (mult - 1))

    return point


def main(file: str):
    image = read_file(file)
    rows_to_expand, cols_to_expand = get_expansion(image)

    points = get_points(image)
    points = [
        expand_point(point, rows_to_expand, cols_to_expand) for point in points
    ]

    distances = get_all_distances(points)

    print(sum(distances))


if __name__ == "__main__":
    main("day11/map.txt")
