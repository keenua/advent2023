from typing import List

def get_diff_line(numbers: List[int]) -> List[int]:
    return [numbers[i] - numbers[i-1] for i in range(1, len(numbers))]

def all_zeros(numbers: List[int]) -> bool:
    return all(n == 0 for n in numbers)

def get_prediction(numbers: List[int]) -> int:
    diffs = [numbers]

    while not all_zeros(diffs[-1]):
        diffs.append(get_diff_line(diffs[-1]))
    diffs[-1].append(0)
    
    # for each diff starting from last one
    for i in range(len(diffs)-2, -1, -1):
        diffs[i].append(diffs[i+1][-1] + diffs[i][-1])

    return diffs[0][-1]


def read_file(file: str) -> List[List[int]]:
    with open(file) as f:
        numbers = [list(map(int, line.split())) for line in f]
    
    return numbers

def main(file: str):
    numbers = read_file(file)

    predictions = [get_prediction(n) for n in numbers]

    print(sum(predictions))

if __name__ == "__main__":
    main("day9/sensors.txt")