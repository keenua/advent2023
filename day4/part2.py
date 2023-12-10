from part1 import read_file


def main(file: str):
    cards = read_file(file)
    cards_count = [1 for _ in cards]

    for i, card in enumerate(cards):
        wins = card.wins()

        if wins == 0:
            continue

        count = cards_count[i]

        for j in range(i + 1, i + wins + 1):
            if j >= len(cards):
                break

            cards_count[j] += count

    print(sum(cards_count))


if __name__ == "__main__":
    main("day4/cards.txt")
