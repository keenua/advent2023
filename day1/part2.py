digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def get_first_digit(line: str) -> int:
    for i in range(len(line)):
        if line[i].isdigit():
            return int(line[i])

        for index, digit in enumerate(digits):
            if line[i:i + len(digit)] == digit:
                return index + 1

    return -1


def get_last_digit(line: str) -> int:
    for i in range(len(line) - 1, -1, -1):
        if line[i].isdigit():
            return int(line[i])

        for index, digit in enumerate(digits):
            if line[i:i + len(digit)] == digit:
                return index + 1

    return -1


def get_calibration_value(line: str) -> int:
    first = get_first_digit(line)
    last = get_last_digit(line)

    res = first * 10 + last
    return res


def main(file: str):
    with open(file) as f:
        lines = f.read().splitlines()

        res = sum([get_calibration_value(line) for line in lines])
        print(res)


if __name__ == "__main__":
    main("day1/calibration.txt")
