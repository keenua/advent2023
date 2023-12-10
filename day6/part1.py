from dataclasses import dataclass
from typing import List


@dataclass
class Race:
    time: int
    distance: int


def read_file(file: str) -> List[Race]:
    with open(file) as f:
        [time_line, distance_line] = f.readlines()

        times = [int(part) for part in time_line.split()[1:]]
        distances = [int(part) for part in distance_line.split()[1:]]

    return [Race(time, distance) for time, distance in zip(times, distances)]


def compute_race(race: Race) -> int:
    count = 0
    for charge in range(race.time):
        distance = (race.time - charge) * charge

        if distance > race.distance:
            count += 1

    return count


def main(file: str):
    races = read_file(file)
    result = 1
    for race in races:
        result *= compute_race(race)
    print(result)


if __name__ == "__main__":
    main("day6/races2.txt")
