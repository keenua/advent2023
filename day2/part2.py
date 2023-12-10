from part1 import load_games, Game, Attempt


def get_min_cubes(game: Game) -> Attempt:
    red = max([attempt.red for attempt in game.attempts])
    green = max([attempt.green for attempt in game.attempts])
    blue = max([attempt.blue for attempt in game.attempts])

    return Attempt(red, green, blue)


def get_power(game: Game) -> int:
    min_cubes = get_min_cubes(game)
    return min_cubes.red * min_cubes.green * min_cubes.blue


def main(file: str):
    games = load_games(file)
    total_power = sum([get_power(game) for game in games])
    print(total_power)


if __name__ == "__main__":
    main("day2/games.txt")
