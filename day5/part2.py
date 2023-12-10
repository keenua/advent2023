from typing import Generator
from part1 import read_file, Segment


def read_seeds(file: str) -> Generator[Segment, None, None]:
    with open(file) as f:
        line = f.readline()

    values = [int(part) for part in line[7:].strip().split(" ")]

    for i in range(0, len(values), 2):
        start = values[i]
        length = values[i + 1]

        yield Segment(start, length)


def main(file: str):
    almanac = read_file(file)
    seeds = read_seeds(file)

    segments = list(seeds)

    for map in almanac.maps:
        new_segments = []
        for segment in segments:
            new_segments.extend(map.map_segment(segment))
        segments = new_segments

    print(min([segment.start for segment in segments]))


if __name__ == "__main__":
    main("day5/almanac.txt")
