import random
import argparse
from typing import Tuple
from enum import Enum


class Difficulty(Enum):
    EASY = {"range": (1, 50), "attempts": 10, "multiplier": 1}
    MEDIUM = {"range": (1, 100), "attempts": 7, "multiplier": 2}
    HARD = {"range": (1, 1000), "attempts": 5, "multiplier": 3}


DIFFICULTIES_BY_NAME = {
    "easy": Difficulty.EASY,
    "medium": Difficulty.MEDIUM,
    "hard": Difficulty.HARD,
}


class GameStats:
    """Track game statistics across multiple rounds."""
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.total_attempts = 0
        self.best_score = 0

    def record_win(self, attempts: int, score: int):
        self.wins += 1
        self.total_attempts += attempts
        if score > self.best_score:
            self.best_score = score

    def record_loss(self):
        self.losses += 1

    def display(self):
        print("\n" + "=" * 40)
        print("GAME STATISTICS")
        print("=" * 40)
        print(f"Wins: {self.wins}")
        print(f"Losses: {self.losses}")
        total_games = self.wins + self.losses
        if total_games > 0:
            win_rate = (self.wins / total_games) * 100
            avg_attempts = self.total_attempts / self.wins if self.wins > 0 else 0
            print(f"Win Rate: {win_rate:.1f}%")
            print(f"Average Attempts: {avg_attempts:.1f}")
        print(f"Best Score: {self.best_score}")
        print("=" * 40 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Play a guess-the-number game")
    parser.add_argument("--debug", action="store_true", help="show the secret number")
    parser.add_argument(
        "--difficulty",
        choices=list(DIFFICULTIES_BY_NAME),
        default=None,
        help="choose difficulty level and skip the menu",
    )
    return parser.parse_args()


def select_difficulty() -> Difficulty:
    """Let user select difficulty level."""
    print("\n" + "=" * 40)
    print("SELECT DIFFICULTY")
    print("=" * 40)
    print("1. Easy   (1-50, 10 attempts)")
    print("2. Medium (1-100, 7 attempts)")
    print("3. Hard   (1-1000, 5 attempts)")
    print("=" * 40)

    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            return Difficulty.EASY
        if choice == "2":
            return Difficulty.MEDIUM
        if choice == "3":
            return Difficulty.HARD

        print("Invalid choice. Please enter 1, 2, or 3.")


def calculate_score(attempts: int, max_attempts: int, multiplier: int) -> int:
    """Calculate score based on attempts and difficulty."""
    if attempts > max_attempts:
        return 0
    remaining = max_attempts - attempts
    return (remaining * 10 + 50) * multiplier


def play(difficulty: Difficulty, debug: bool = False) -> Tuple[bool, int, int]:
    """Run the interactive guessing loop. Returns (guessed, score, attempts)."""
    config = difficulty.value
    min_num, max_num = config["range"]
    max_attempts = config["attempts"]
    multiplier = config["multiplier"]

    number = random.randint(min_num, max_num)
    if debug:
        print(f"(debug) secret number = {number}")

    attempts = 0
    hints_used = 0

    print(f"\nGuess the number between {min_num} and {max_num}!")
    print(f"You have {max_attempts} attempts.\n")

    while attempts < max_attempts:
        attempts += 1
        raw = input(
            f"Attempt {attempts}/{max_attempts} - Enter guess (or 'h' for hint): "
        ).strip().lower()

        if raw == "h":
            if hints_used < 2:
                midpoint = (min_num + max_num) // 2
                if number > midpoint:
                    print("Hint: The number is in the UPPER half!")
                else:
                    print("Hint: The number is in the LOWER half!")
                hints_used += 1
            else:
                print("No more hints available!")
            attempts -= 1
            continue

        try:
            guess = int(raw)
        except ValueError:
            print("Please enter a valid integer.")
            attempts -= 1
            continue

        if not min_num <= guess <= max_num:
            print(f"Please guess a number between {min_num} and {max_num}.")
            attempts -= 1
            continue

        if guess == number:
            score = calculate_score(attempts, max_attempts, multiplier)
            print(f"\nYou got it in {attempts} attempt{'s' if attempts != 1 else ''}!")
            print(f"Score: {score}")
            return True, score, attempts

        if guess < number:
            print("Too low! The number is higher.")
        else:
            print("Too high! The number is lower.")

    print(f"\nOut of attempts - the number was {number}.")
    return False, 0, attempts


def main():
    args = parse_args()
    stats = GameStats()

    print("\n" + "=" * 40)
    print("WELCOME TO THE GUESSING GAME!")
    print("=" * 40)

    while True:
        if args.difficulty:
            difficulty = DIFFICULTIES_BY_NAME[args.difficulty]
        else:
            difficulty = select_difficulty()

        won, score, attempts = play(difficulty, args.debug)

        if won:
            stats.record_win(attempts, score)
        else:
            stats.record_loss()

        play_again = input("\nPlay again? (yes/no): ").strip().lower()
        if play_again not in ["yes", "y"]:
            stats.display()
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
