# Number Guessing Game

A simple CLI game to test your luck. The computer picks a number between 1 and 100, and you try to guess it before you run out of chances.

## Features

- Three difficulty levels: Easy (10 chances), Medium (5), Hard (3)
- "Greater than / less than" feedback after every wrong guess
- Play multiple rounds without restarting
- Timer showing how long you took to win
- Hint system: type `hint` (max 2 per round, free of charge)
- Persistent high scores (fewest attempts per difficulty)

## Requirements

Python 3.6+ (standard library only, nothing to install).

## How to run

```bash
python3 number_guessing_game.py
```

## Sample session

```
Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.

Please select the difficulty level:
1. Easy (10 chances)
2. Medium (5 chances)
3. Hard (3 chances)

Enter your choice: 2

Great! You have selected the Medium difficulty level.
Let's start the game!

Enter your guess: 50
Incorrect! The number is less than 50.

Enter your guess: 30
Congratulations! You guessed the correct number in 2 attempts.
```

## High scores

Scores are saved to `highscores.json` in the same folder as the script. Delete the file to reset them.

## License

MIT
