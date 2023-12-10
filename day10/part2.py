from typing import List, Tuple

from part1 import read_file, traverse

CELL = Tuple[int, int]


def winding_number(point: CELL, loop: List[CELL]) -> int:
    winding_number = 0
    point_x, point_y = point

    for index, loop_point in enumerate(loop):
        if index == 0:
            continue

        prev_point = loop[index - 1]
        loop_point_x, loop_point_y = loop_point
        prev_point_x, prev_point_y = prev_point

        if prev_point_y <= point_y and loop_point_y > point_y:
            if (loop_point_x - prev_point_x) * (point_y - prev_point_y) - (
                point_x - prev_point_x
            ) * (loop_point_y - prev_point_y) > 0:
                winding_number += 1
        elif prev_point_y > point_y and loop_point_y <= point_y:
            if (loop_point_x - prev_point_x) * (point_y - prev_point_y) - (
                point_x - prev_point_x
            ) * (loop_point_y - prev_point_y) < 0:
                winding_number -= 1

    return winding_number


def main(file: str):
    maze = read_file(file)
    traverse(maze, 1)

    inside = 0
    for x in range(maze.width):
        for y in range(maze.height):
            if maze.part_of_the_loop[y][x]:
                continue

            if winding_number((x, y), maze.loop_path) != 0:
                inside += 1

    print(inside)


if __name__ == "__main__":
    main("day10/maze.txt")
