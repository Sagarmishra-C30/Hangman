# Hangman Game

Hangman is a classic word-guessing game where players try to guess a hidden word by suggesting letters or guessing the entire word. This implementation of Hangman is a command-line game written in Python. It supports both single-player and two-player modes.

## How to Play

1. Run the Python script `hangman.py` to start the game.
2. You will be prompted to choose the game mode:
   - Enter "1" for single-player mode.
   - Enter "2" for two-player mode.
   - Enter "exit" to exit the game.
3. If you choose single-player mode:
   - Select the difficulty level: easy, normal, or hard.
   - Enter a word of 2 to 7 characters for the other player to guess.
   - The game will begin, and you need to guess the word within the given number of lives.
4. If you choose two-player mode:
   - Enter the names of the two players.
   - Select the difficulty level: easy, normal, or hard.
   - The first player will be prompted to enter a word for the second player to guess.
   - The game will alternate between the two players until both have guessed a word.
5. During the game, you can guess a letter or the entire word.
6. If you guess a letter:
   - If the letter is present in the word, it will be revealed in its correct position(s).
   - If the letter is not present, you will lose a life.
7. If you guess the entire word correctly, you win the game.
8. If you run out of lives before guessing the word, you lose the game.
9. After the game ends, you will be asked if you want to play again.

## Scoring

In two-player mode, the game keeps track of each player's score. The player who guesses the word correctly earns one point. At the end of the game, the scores of both players are displayed, and the winner is announced. If both players have the same score, it is considered a draw.

## Difficulty Levels

The game offers three difficulty levels: easy, normal, and hard. Each level has a different number of lives:

- Easy: 10 lives
- Normal: 7 lives
- Hard: 3 lives

Choose the difficulty level based on your preference and skill level.

## Additional Notes

- The game uses the `getpass` module to hide the word input while taking input from the players, preventing cheating.
- The game reads a list of words from a file named `words.txt`. Ensure this file is present in the same directory as the script. The file should contain one word per line.
- The game handles invalid input, such as empty strings, numbers, or spaces, and provides appropriate error messages.
- To clear the console screen during the game, you can enter "cls" as a response.
- The game uses Unicode character "\u2665" to display a heart symbol as a representation of lives.

Have fun playing Hangman!