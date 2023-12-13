from typing import List, Tuple

ROW = Tuple[str, List[int]]

DEBUG = False


def get_combinations(row: ROW) -> int:
    result = 0

    data, sizes = row

    if DEBUG:
        print("--------ROW--------")
        print(sizes)
        print(data)

    rows = [(data, sizes, "")]
    generated: List[str] = []

    while len(rows) > 0:
        data, sizes, prev = rows.pop(0)
        size = sizes.pop(0)

        right = sum(sizes) + len(sizes) - 1
        last_index = len(data) - right
        for i in range(last_index - size):
            if i > 0 and data[i - 1] == "#":
                continue

            if "." in data[i : i + size]:
                continue

            if i + size < len(data) and data[i + size] == "#":
                continue

            if "#" in data[0:i]:
                continue

            if DEBUG:
                new_prev = (prev + ".") if prev else ""
                new_prev = new_prev + data[:i].replace("?", ".") + ("#" * size)
            else:
                new_prev = ""

            if len(sizes) == 0:
                if "#" in data[i + size :]:
                    continue

                if DEBUG:
                    generated.append(new_prev + data[i + size :].replace("?", "."))

                result += 1
                continue

            new_data = data[i + size + 1 :]
            new_sizes = sizes.copy()
            rows.append((new_data, new_sizes, new_prev))

    if DEBUG:
        for row in generated:
            print(row)

        input()

    return result


def read_file(file: str) -> List[ROW]:
    result = []

    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            data, sizes = line.split(" ")
            sizes = [int(size) for size in sizes.split(",")]
            result.append((data, sizes))

    return result


def main(file: str):
    rows = read_file(file)

    result = sum([get_combinations(row) for row in rows])
    print(result)


if __name__ == "__main__":
    main("day12/springs.txt")
