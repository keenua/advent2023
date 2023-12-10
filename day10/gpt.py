from part1 import read_file


def find_points_inside_loop(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False]*cols for _ in range(rows)]
    loop = set()

    # Perform flood fill from a point outside the loop
    def flood_fill(i, j):
        if i < 0 or i >= rows or j < 0 or j >= cols or visited[i][j] or grid[i][j] != '.':
            return
        visited[i][j] = True
        flood_fill(i-1, j)
        flood_fill(i+1, j)
        flood_fill(i, j-1)
        flood_fill(i, j+1)

    flood_fill(0, 0)

    # Find points inside the loop
    inside_points = set()
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and grid[i][j] == '.':
                inside_points.add((i, j))

    # Exclude points in the "holes" of the loop
    for point in inside_points.copy():
        visited = [[False]*cols for _ in range(rows)]
        stack = [point]
        while stack:
            i, j = stack.pop()
            if i < 0 or i >= rows or j < 0 or j >= cols or visited[i][j]:
                continue
            visited[i][j] = True
            if grid[i][j] != '.':
                inside_points.remove(point)
                break
            stack.extend([(i-1, j), (i+1, j), (i, j-1), (i, j+1)])

    return inside_points


def main(file: str):
    maze = read_file(file)
    points = find_points_inside_loop(maze.matrix)
    print(len(points))


if __name__ == "__main__":
    main("day10/test8.txt")
