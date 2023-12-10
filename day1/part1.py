def get_calibration_value(line: str) -> int:
    first = None
    last = None

    for char in line:
        if char.isdigit():
            if first is None:
                first = char
            last = char

    return int(first + "" + last)


def main(file: str):
    with open(file) as f:
        lines = f.read().splitlines()

        res = sum([get_calibration_value(line) for line in lines])
        print(res)


if __name__ == "__main__":
    main("day1/calibration.txt")
