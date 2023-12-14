from dataclasses import dataclass
from typing import Any, List, Tuple
from os import system

import numpy as np
from part1 import INV_CELLS, PLATFORM, CELLS, calculate_load, print_platform, read_file
from colorama import Back

DEBUG = False

CLEAR = lambda: system("cls")

MEMO = {}
MEMO_BY_INDEX = {}
CYCLE_INDEX = 0
CYCLES = 1000000000

@dataclass
class Gap:
    start: int
    length: int
    is_vertical: bool
    index: int

    def __str__(self):
        return f"Gap({self.start}, {self.length}, {self.is_vertical}, {self.index})"

    def select(self, platform: PLATFORM) -> np.ndarray:
        grid = platform.T if self.is_vertical else platform
        return grid[self.index, self.start:self.start+self.length]

    def count_rocks(self, platform: PLATFORM) -> int:
        gap = self.select(platform)
        return np.sum(gap)
    
    def to_coords(self) -> List[Tuple[int, int]]:
        if self.is_vertical:
            return [(self.start + i, self.index) for i in range(self.length)]
        else:
            return [(self.index, self.start + i) for i in range(self.length)]

    def pack(self, platform: PLATFORM, left: bool):
        count = self.count_rocks(platform)
        
        if DEBUG:
            CLEAR()
            print(self)
            print()
            self.print(platform)
            print()

        if left:
            if self.is_vertical:
                platform[self.start:self.start+count, self.index] = CELLS["O"]
                platform[self.start+count:self.start+self.length, self.index] = CELLS["."]
            else:
                platform[self.index, self.start:self.start+count] = CELLS["O"]
                platform[self.index, self.start+count:self.start+self.length] = CELLS["."]
        else:
            if self.is_vertical:
                platform[self.start:self.start+self.length-count, self.index] = CELLS["."]
                platform[self.start+self.length-count:self.start+self.length, self.index] = CELLS["O"]    
            else:
                platform[self.index, self.start:self.start+self.length-count] = CELLS["."]
                platform[self.index, self.start+self.length-count:self.start+self.length] = CELLS["O"]
        
        if DEBUG:
            self.print(platform)
            input()

        new_count = self.count_rocks(platform)
        assert count == new_count, f"Count mismatch: {count} != {new_count}"

    def print(self, platform: PLATFORM):
        coords = self.to_coords()

        for r, row in enumerate(platform):
            for c, col in enumerate(row):
                if (r, c) in coords:
                    print(Back.GREEN + INV_CELLS[col], end="")
                    print(Back.RESET, end="")
                else:
                    print(INV_CELLS[col], end="")
            print()
        
        print()


def plaform_hash(platform: PLATFORM) -> str:
    return "".join([INV_CELLS[c] for c in platform.flatten()])


def get_gaps(row: List[int], is_vertical: bool, other: int) -> List[Gap]:
    start = -1
    result = []

    for i, item in enumerate(row):
        if item == CELLS["#"]:
            if start == -1:
               continue

            if start != i:
                result.append(Gap(start, i - start, is_vertical, other))
            start = i + 1
        else:
            if start == -1:
                start = i

    if start != len(row):
        result.append(Gap(start, len(row) - start, is_vertical, other))

    return result

def flat(arr: List[List[Any]]) -> List[Any]:
    return [item for sublist in arr for item in sublist]



def cycle(platform: PLATFORM, hor_gaps: List[Gap], ver_gaps: List[Gap]) -> int:
    global CYCLE_INDEX

    phash = plaform_hash(platform)
    
    # NORTH
    for gap in ver_gaps:
        gap.pack(platform, True)

    # WEST
    for gap in hor_gaps:
        gap.pack(platform, True)

    # SOUTH
    for gap in ver_gaps:
        gap.pack(platform, False)

    # EAST
    for gap in hor_gaps:
        gap.pack(platform, False)

    load = calculate_load(platform)

    if phash in MEMO:
        prev, _ = MEMO[phash]
        loop_length = CYCLE_INDEX - prev
        offset = (CYCLES - prev) % loop_length
        actual = prev + offset - 1
        return MEMO_BY_INDEX[actual]
    else:
        MEMO[phash] = CYCLE_INDEX, load
        MEMO_BY_INDEX[CYCLE_INDEX] = load

    CYCLE_INDEX += 1

    return -1
    

def main(file: str):
    platform = read_file(file)
    print_platform(platform)
    print()

    hor_gaps = flat([get_gaps(row, False, i) for i, row in enumerate(platform)])
    ver_gaps = flat([get_gaps(row, True, i) for i, row in enumerate(platform.T)])

    for _ in range(CYCLES):
        res = cycle(platform, hor_gaps, ver_gaps)
        if res != -1:
            print("RESULT", res)
            break

        print(calculate_load(platform))
    
    print()


if __name__ == "__main__":
    main("day14/platform.txt")
    