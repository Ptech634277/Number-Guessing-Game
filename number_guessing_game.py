#!/usr/bin/env python3
"""Number Guessing Game - a simple CLI game to test your luck.

Features: difficulty levels, multiple rounds, timer, hints, persistent high scores.
Run with:  python3 number_guessing_game.py
"""

import json
import random
import time
from pathlib import Path

LOW, HIGH = 1, 100
DIFFICULTIES = {"1": ("Easy", 10), "2": ("Medium", 5), "3": ("Hard", 3)}
MAX_HINTS = 2
SCORE_FILE = Path(__file__).with_name("highscores.json")


# ---------- high scores ----------
def load_scores():
    try:
        return json.loads(SCORE_FILE.read_text())
    except (OSError, ValueError):
        return {}


def save_scores(scores):
    try:
        SCORE_FILE.write_text(json.dumps(scores, indent=2))
    except OSError:
        print("(Could not save high scores.)")


# ---------- hints ----------
def build_hints(secret):
    """Return a shuffled list of hint strings for the secret number."""
    hints = [f"The number is {'even' if secret % 2 == 0 else 'odd'}."]
    for d in (3, 5, 7):
        if secret % d == 0:
            hints.append(f"The number is divisible by {d}.")
            break
    else:
        hints.append("The number is not divisible by 3, 5 or 7.")
    start = max(LOW, min(secret - random.randint(2, 18), HIGH - 19))
    hints.append(f"The number is between {start} and {start + 19}.")
    hints.append(f"The sum of the digits is {sum(map(int, str(secret)))}.")
    random.shuffle(hints)
    return hints


# ---------- input helpers ----------
def choose_difficulty():
    print("Please select the difficulty level:")
    for key, (name, chances) in DIFFICULTIES.items():
        print(f"{key}. {name} ({chances} chances)")
    while True:
        choice = input("\nEnter your choice: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Invalid choice. Please enter 1, 2 or 3.")


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


# ---------- one round ----------
def play_round(scores):
    secret = random.randint(LOW, HIGH)
    name, chances = choose_difficulty()
    hints = build_hints(secret)[:MAX_HINTS]
    hints_used = 0

    print(f"\nGreat! You have selected the {name} difficulty level.")
    print(f"You have {chances} chances to guess the number.")
    print(f"Type 'hint' for a clue (max {MAX_HINTS}, hints don't cost a chance).")
    print("Let's start the game!\n")

    attempts = 0
    start = time.time()

    while attempts < chances:
        raw = input("Enter your guess: ").strip().lower()

        if raw == "hint":
            if hints_used < len(hints):
                print(f"Hint: {hints[hints_used]}\n")
                hints_used += 1
            else:
                print("No hints left!\n")
            continue

        if not raw.lstrip("-").isdigit() or not LOW <= int(raw) <= HIGH:
            print(f"Please enter a whole number between {LOW} and {HIGH}.\n")
            continue

        guess = int(raw)
        attempts += 1

        if guess == secret:
            elapsed = time.time() - start
            word = "attempt" if attempts == 1 else "attempts"
            print(f"Congratulations! You guessed the correct number in {attempts} {word}.")
            print(f"Time taken: {elapsed:.1f} seconds.")
            best = scores.get(name)
            if best is None or attempts < best:
                scores[name] = attempts
                save_scores(scores)
                print(f"New high score for {name}: {attempts} {word}!")
            else:
                print(f"High score for {name}: {best} attempts.")
            return

        direction = "less" if secret < guess else "greater"
        print(f"Incorrect! The number is {direction} than {guess}.")
        remaining = chances - attempts
        if remaining:
            print(f"({remaining} {'chance' if remaining == 1 else 'chances'} left)\n")

    print(f"\nSorry, you're out of chances! The number was {secret}.")


# ---------- main ----------
def main():
    print("Welcome to the Number Guessing Game!")
    print(f"I'm thinking of a number between {LOW} and {HIGH}.")
    print("Pick a difficulty to decide how many chances you get.\n")

    scores = load_scores()
    try:
        while True:
            play_round(scores)
            if not ask_yes_no("\nDo you want to play again? (y/n): "):
                break
            print()
    except (KeyboardInterrupt, EOFError):
        print()
    print("Thanks for playing. Goodbye!")


if __name__ == "__main__":
    main()
