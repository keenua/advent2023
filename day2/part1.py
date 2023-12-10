from dataclasses import dataclass
from typing import List


@dataclass
class Attempt:
    red: int
    green: int
    blue: int


@dataclass
class Game:
    id: int
    attempts: List[Attempt]


def parse_attempt(attempt: str) -> Attempt:
    red = 0
    green = 0
    blue = 0

    colors = attempt.split(", ")
    for color in colors:
        count = int(color.split(" ")[0])
        if color.endswith("red"):
            red = count
        elif color.endswith("green"):
            green = count
        elif color.endswith("blue"):
            blue = count

    return Attempt(red, green, blue)


def load_games(file: str) -> List[Game]:
    with open(file) as f:
        lines = f.readlines()
        games = []
        for line in lines:
            id = line.split(": ")[0].split(" ")[1]
            attempts = line.split(": ")[1].strip().split("; ")
            attempts = [parse_attempt(attempt) for attempt in attempts]
            games.append(Game(id, attempts))

        return games


def is_possible(game: Game) -> bool:
    for attempt in game.attempts:
        if attempt.red > 12 or attempt.green > 13 or attempt.blue > 14:
            return False

    return True


def main(file: str):
    games = load_games(file)
    sum_of_ids = sum([int(game.id) for game in games if is_possible(game)])
    print(sum_of_ids)


if __name__ == "__main__":
    main("day2/games.txt")
