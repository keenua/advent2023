from dataclasses import dataclass
from typing import List, Set


@dataclass
class Card:
    id: int
    winning_numbers: Set[int]
    numbers: Set[int]

    def wins(self) -> int:
        return len(self.winning_numbers.intersection(self.numbers))


def score(card: Card) -> int:
    wins = card.wins()
    if wins == 0:
        return 0
    return 2 ** (wins - 1)


def parse_card(card: str) -> Card:
    parts = card.split(": ")
    id = int(parts[0].split(" ")[-1])

    [win, num] = parts[1].split("|")

    winning_numbers = set(
        [int(number.strip()) for number in win.strip().split(" ") if number]
    )
    numbers = set([int(number.strip()) for number in num.strip().split(" ") if number])
    return Card(id, winning_numbers, numbers)


def read_file(file: str) -> List[Card]:
    with open(file) as f:
        return [parse_card(card) for card in f.readlines()]


def main(file: str):
    cards = read_file(file)
    points = sum([score(card) for card in cards])
    print(points)


if __name__ == "__main__":
    main("day4/cards.txt")
