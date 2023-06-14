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
   - Then select one category that you would like to play.
   - A random word word of 3 to 20 will be chosen by computer based on difficulty level, for the player to guess.
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
   - If the letter is already guess nothing would change (u won't lose your life for reguessing the same letter.) 
7. If you guess the entire word correctly, you win the game.
8. If you run out of lives before guessing the word, you lose the game.
9. You will have 15 sec per guess. If u guess a letter after 15 sec expires, u will lose 1 life.
10. A single round of game lasts 2 min, if u take any longer to guess, u lose.
9. After the game ends, you will be asked if you want to play again.

## Scoring

In two-player mode, the game keeps track of each player's score. The player who guesses the word correctly earns one point. At the end of the game, the scores of both players are displayed, and the winner is announced. If both players have the same score, it is considered a draw.

## Difficulty Levels

The game offers three difficulty levels: easy, normal, and hard. Each level has a different number of lives:

- Easy: 10 lives, word-length: 3 to 10
- Normal: 7 lives, word-length: 6 to 12
- Hard: 3 lives, word-length: 10 to 20

Choose the difficulty level based on your preference and skill level.

## Additional Notes

- The game uses the `getpass` module to hide the word input while taking input from the players, preventing cheating.
- The game reads a list of words from different files in words folder, based on the category u chose to play. Ensure this folder is present in the same directory as the script. The file should contain one word per line.
- The game handles invalid input, such as empty strings, numbers, or spaces, and provides appropriate error messages.
- To clear the console screen during the game, you can enter "cls" as a response.
- The game uses Unicode character "\u2665" to display a heart symbol as a representation of lives.
- Remaning time and total life remaining so far will be displayed after each guess to help user keep track of their stats.
- different ASCII art is used for winners and losers.
Have fun playing Hangman!

## Contributing

Contributions to the Hangman Game project are welcome and encouraged! If you would like to contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

Please ensure that your code adheres to the existing coding style and conventions used in the project.