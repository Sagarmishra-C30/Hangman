#guess the word. with lives u have
import random
import re
import os
import getpass
import sys

if sys.stdout.encoding is None:
    # Set the default encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

heart = '\u2665'  # unicode char for heart
Player1 = True
Player2 = False
score1, score2 = 0, 0
num_players = 1

def difficulty():
    # Set difficulty level
    difficulty = input('Choose difficulty level:\na) Easy[e]\t\tb) Normal[n]\t\tc) Hard[h]\n').strip()
    if difficulty.lower() in ['hard', 'h']:
        lives = 3
    elif difficulty.lower() in ['normal', 'n']:
        lives = 7
    else:
        lives = 10
    return lives

def score():
    # Score of player
    global Player1, Player2, score1, score2
    if Player1:
        score1 += 1
    elif Player2:
        score2 += 1

def display_score():
    # Display score, winner, and loser
    if score1 > score2:
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\n\n' +
        f'{"*"*20}  Winner is {player1_name}  {"*"*20}'.center(100) + '\n')
    elif score1 < score2:
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\n\n' + 
        f'{"*"*20}  Winner is {player2_name}  {"*"*20}'.center(100) + '\n')
    else:
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\n\n' +
        f'{"*"*20}  Draw  {"*"*20}'.center(100) + '\n')

def deduct(lives, fill_word):
    # Deduct player's life if guessed wrong
    print(fill_word)
    lives -= 1
    print(f'1 live deducted. Lives left: {lives}\t{heart * lives}'.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
    return lives

def taking_input(player_name):
    # Take input and hide the input while taking input so that other player doesn't cheat
    string = getpass.getpass(prompt=f'Enter your word, {player_name}:\n>> ').strip()
    string_regex = re.compile(r'[0-9]+|\s+').search(string)
    if string_regex is not None:
        print('Enter only a word, no number or space is allowed.\n')
        print(f'Your word: {string}')
        exit()
    else:
        return string.lower()

def play_again():
    # Ask player whether to play again or not
    while True:
        response = input('\nDo you want to play again?\nType - a) Yes[y]\t\tb) No\t\t"cls" - to clear screen:\n>>')
        if response.lower() == 'yes' or response.lower() == 'y':
            one_player() if num_players == 1 else two_player()
        elif response.lower() == 'cls':
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')
        else:
            print('Thank you for playing.')
            exit()

def next_player():
    # Selects next player and take input by calling taking_input function
    global Player1, Player2
    if Player1:
        string = taking_input(player1_name)
        Player1 = False
        Player2 = True
    elif Player2:
        string = taking_input(player2_name)
        Player2 = False
        Player1 = True
    return string

def one_player():
    global dif, num_players, player1_name, player2_name
    num_players = 1
    # Open a file and randomly select a string
    with open('words.txt') as f:
        file = f.read()
        file_list = file.split('\n')
        # Select one word from the list of 11000+ words
        string = (random.choice(file_list)).lower()
        if len(string) < 3 or len(string) > 15:
            one_player()  # Calling itself
        else:
            word_guess(string, dif, num_players)
            play_again()  # Ask player if they want to play again

counting_ = 0

def two_player():
    global counting_, dif, num_players, player1_name, player2_name
    num_players = 2
    string = next_player()
    word_guess(string, dif, num_players)
    counting_ += 1
    # If both players have had their chance, ask if they want to play further. If only one player played, let the other player play too
    if counting_ % 2 == 0:
        res = input('Do you want to continue playing?\nYes[y]\t\tNo[n]\t\t"cls" - to clear screen\n>> ').strip()
        if res.lower() in ['yes', 'y']:
            two_player()
        elif res.lower() == 'cls':
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')
        else:
            display_score()
            print('Thanks for playing.')
            exit()
    else:
        two_player()
        

def create_fill_word(string):
    return ['__' for _ in string]

def process_guess(guess, string, fill_word, lives):
    if guess == '':
        print('Empty string not allowed.\n')
        return lives

    if guess.isdigit():
        print('Enter a letter or a string.\n')
        return lives - 1

    if guess in string:
        for index, letter in enumerate(string):
            if letter == guess:
                fill_word[index] = guess
        return lives

    return lives - 1

def is_word_complete(fill_word, word):
    return fill_word == word

def word_guess(string, lives=10, number_of_player=1):
    num_players = number_of_player
    word = list(string)
    fill_word = create_fill_word(string)

    print(' '.join(fill_word))
    print()

    while lives > 0:
        guess = input('Guess a letter or the whole word:\n>> ').strip().lower()
        if guess == string:
            print('You won') if num_players == 1 else score()
            return
            
        lives = process_guess(guess, string, fill_word, lives)
        
        print(' '.join(fill_word))

        if is_word_complete(fill_word, word):
            print('You won') if num_players == 1 else score()
            return

        print(f'Total lives: {lives}\t{heart * lives}\n'.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))

    print(f'Your lives are over. You lose.\nThe correct word is \'{string}\'.\nBetter luck next time.\n\n')




if __name__ == "__main__":
    print('\n' + f'{"*"*10}  welcome to the Hangman Game  {"*"*10}'.center(100) + '\n\n')
    play = input('"1"- for 1-Player game\t\t"2" for 2-Player game\t\t"exit" - to exit the game\n>> ').strip()
    if play == '1':
        dif = difficulty()
        print()
        one_player()
    elif play == '2':
        player1_name = input("enter your name player 1:\n>> ")
        player2_name = input("enter your name player 2:\n>> ")
        dif = difficulty()
        two_player()
    else:
        exit()

    