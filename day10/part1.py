from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Direction:
    x: int
    y: int

    def is_opposite(self, other: "Direction") -> bool:
        return self.x == -other.x and self.y == -other.y

    def left(self) -> "Direction":
        return Direction(-self.y, self.x)

    def right(self) -> "Direction":
        return Direction(self.y, -self.x)

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def move(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        (x, y) = pos
        return (x + self.x, y + self.y)


LEFT = Direction(-1, 0)
RIGHT = Direction(1, 0)
UP = Direction(0, -1)
DOWN = Direction(0, 1)


@dataclass
class Maze:
    matrix: List[str]
    shortest_dist: List[List[int]]
    part_of_the_loop: List[List[bool]]
    width: int
    height: int
    start: Tuple[int, int]
    loop_path: List[Tuple[int, int]]

    def contains(self, pos: Tuple[int, int]) -> bool:
        (x, y) = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def get_possible_dirs(self, pos: Tuple[int, int]) -> List["Direction"]:
        if not self.contains(pos):
            return []

        (x, y) = pos

        symbol = self.matrix[y][x]

        if symbol == "7":
            return [LEFT, DOWN]
        elif symbol == "L":
            return [RIGHT, UP]
        elif symbol == "J":
            return [LEFT, UP]
        elif symbol == "F":
            return [RIGHT, DOWN]
        elif symbol == "-":
            return [LEFT, RIGHT]
        elif symbol == "|":
            return [UP, DOWN]

        return []


def get_possible_start_directions(maze: Maze) -> List[Direction]:
    (x, y) = maze.start

    result = []

    if LEFT in maze.get_possible_dirs((x + 1, y)):
        result.append(RIGHT)
    if RIGHT in maze.get_possible_dirs((x - 1, y)):
        result.append(LEFT)
    if UP in maze.get_possible_dirs((x, y + 1)):
        result.append(DOWN)
    if DOWN in maze.get_possible_dirs((x, y - 1)):
        result.append(UP)

    assert len(result) == 2

    return result


def read_file(file: str) -> Maze:
    matrix: List[str] = []
    start = (0, 0)

    with open(file, "r") as f:
        for line in f:
            row = line.strip()
            if "S" in row:
                start = (row.index("S"), len(matrix))
            matrix.append(row)

    width = len(matrix[0])
    height = len(matrix)
    shortest_dist = [[width * height for _ in range(width)] for _ in range(height)]
    part_of_the_loop = [[False for _ in range(width)] for _ in range(height)]

    return Maze(matrix, shortest_dist, part_of_the_loop, width, height, start, [])


def traverse(maze: Maze, direction_index: int) -> int:
    pos = maze.start
    (x, y) = pos

    visited = set()
    visited.add(pos)
    maze.loop_path.append(pos)
    maze.part_of_the_loop[y][x] = True

    distance = 0
    maze.shortest_dist[y][x] = distance
    direction = get_possible_start_directions(maze)[direction_index]

    result = 0

    represent: List[str] = ["." * maze.width for _ in range(maze.height)]
    represent[y] = represent[y][:x] + "S" + represent[y][x + 1 :]

    while True:
        # move in the direction
        pos = direction.move(pos)
        (x, y) = pos
        distance += 1

        maze.shortest_dist[y][x] = min(distance, maze.shortest_dist[y][x])
        maze.part_of_the_loop[y][x] = True
        maze.loop_path.append(pos)
        represent[y] = represent[y][:x] + maze.matrix[y][x] + represent[y][x + 1 :]

        # clear console
        # print("\033c")
        # for row in represent:
        #     print(row)
        # input()

        result = max(result, maze.shortest_dist[y][x])

        if pos in visited:
            break

        possible_directions = maze.get_possible_dirs(pos)
        non_opposite = [d for d in possible_directions if not direction.is_opposite(d)]

        assert len(non_opposite) == 1

        direction = non_opposite[0]
        visited.add(pos)

    return result


def main(file: str):
    maze = read_file(file)
    traverse(maze, 0)
    result = traverse(maze, 1)

    print(result)


if __name__ == "__main__":
    main("day10/maze.txt")
