from typing import List
from part1 import all_zeros, get_diff_line, read_file

def get_prediction(numbers: List[int]):
    diffs = [numbers]

    while not all_zeros(diffs[-1]):
        diffs.append(get_diff_line(diffs[-1]))
    diffs[-1].insert(0, 0)
    
    for i in range(len(diffs)-2, -1, -1):
        diffs[i].insert(0, diffs[i][0] - diffs[i+1][0])

    return diffs[0][0]


def main(file: str):
    numbers = read_file(file)

    predictions = [get_prediction(n) for n in numbers]

    print(sum(predictions))

if __name__ == "__main__":
    main("day9/sensors.txt")