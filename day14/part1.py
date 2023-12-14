from typing import List
import numpy as np

CELLS = {
    ".": 0,
    "O": 1,
    "#": 2
}

INV_CELLS = {
    0: ".",
    1: "O",
    2: "#"
}

PLATFORM = np.ndarray

def read_file(file: str) -> PLATFORM:
    with open(file, "r") as f:
        c = [[CELLS[c] for c in line.strip()] for line in f.readlines()]
        return np.array(c)


def print_platform(platform: PLATFORM):
    for r in platform:
        for c in r:
            print(INV_CELLS[c], end="")
        
        print()

def tilt_north(platform: PLATFORM) -> PLATFORM:
    width, height = platform.shape

    result = platform.copy()

    for col in range(width):
        for row in range(height - 1):
            if result[row][col] != CELLS["."]:
                continue

            south = row + 1
            while south < height and result[south][col] == CELLS["."]:
                south += 1

            if south == height:
                break

            if result[south][col] != CELLS["O"]:
                continue
            
            result[row][col] = CELLS["O"]
            result[south][col] = CELLS["."]

    return result


def calculate_load(platform: PLATFORM) -> int:
    result = 0
    height = platform.shape[0]

    for r, row in enumerate(platform):
        for col in row:
            if col == CELLS["O"]:
                result += height - r

    return result


def main(file: str):
    platform = read_file(file)
    print_platform(platform)
    print()

    tilted = tilt_north(platform)
    print_platform(tilted)
    print()

    load = calculate_load(tilted)
    print(load)
   
if __name__ == "__main__":
    main("day14/test.txt")
    
