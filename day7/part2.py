from typing import Generator, Tuple
from collections import Counter

ranks = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
ranks_map = {rank: index for index, rank in enumerate(ranks)}


def get_type(hand_str: str) -> int:
    if hand_str.count("J") == 5:
        return 7

    counter = Counter(hand_str.replace("J", ""))

    best = counter.most_common(2)
    top1 = best[0][1] + hand_str.count("J")

    if top1 == 5:
        return 7
    elif top1 == 4:
        return 6
    elif top1 == 3:
        if best[1][1] == 2:
            return 5
        else:
            return 4
    elif top1 == 2:
        if best[1][1] == 2:
            return 3
        else:
            return 2
    else:
        return 1


def encode_hand(hand_str: str) -> int:
    hand_type = get_type(hand_str)
    card_values = [ranks_map[card] for card in hand_str]

    value = 0
    multiplier = 1
    for card_value in card_values[::-1]:
        value += card_value * multiplier
        multiplier *= 13

    return hand_type * multiplier + value


def read_file(file: str) -> Generator[Tuple[int, int, str], None, None]:
    with open(file) as f:
        for line in f:
            [hand, bid] = line.split()
            yield (encode_hand(hand), int(bid), hand)


def main(file: str):
    hands = read_file(file)
    hands = sorted(hands, key=lambda hand: hand[0])

    total = 0
    for index, hand in enumerate(hands):
        print(index, hand[0], hand[2], hand[1])
        total += (index + 1) * hand[1]

    print(total)


if __name__ == "__main__":
    main("day7/hands.txt")
