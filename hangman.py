#guess the word. with lives u have
import random
import re, os
import getpass
import sys

if sys.stdout.encoding is None:
    # Set the default encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

heart = heart = '\u2665' # unicode char for heart
Player1 = True
Player2 = False
score1, score2 = 0, 0

def difficulty():
    #set difficulty level
    difficulty = input('choose difficulty level:\na)easy[e]\t\tb)normal[n]\t\tc)hard[h]\n').strip()
    if difficulty.lower() in ['hard','h']:
        lives = 3
    elif difficulty.lower() in ['normal','n']:
        lives = 7
    else:
        lives = 10
    return lives

def score():
    # score of player
    global Player1, Player2, score1, score2
    if Player1:
        score1 += 1
    elif Player2:
        score2 += 1

def display_score():
    # display score ..winner and looser
    if score1 > score2:
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\n Winner is {player1_name}\n')
    elif score1 < score2:
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\n Winner is {player2_name}\n')
    else:
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\nDraw\n')
  
def deduct(live,fill):
    # deduct players life if guessed wrong
    print(fill)
    lives = live - 1
    print(f'1 live deducted. lives left {lives}\t{heart * lives}'.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
    return lives

def taking_input():
    # take input and hide the input while taking input so that other player doesnt cheat
    string = getpass.getpass(prompt = f'enter your word {player1_name if Player1 else player2_name}:\n>> ').strip()
    string_regex = re.compile(r'[0-9]+|\s+').search(string)
    if string_regex != None:
        print('enter only a word, no number or space is allowed.\n')
        print(f'your word {string}')
        exit()
    else:
        return string

def play_again_1():
    # ask player whether to play again or not.
    while True:
        response = input('\nDo u wanna play again?\ntype - a)yes(y)\t\tb)no\t\t"cls" - to clear screen:\n>>')
        if response.lower() == 'yes' or response.lower() == 'y':
            one_player()
        elif response.lower() == 'cls':
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')
        else:
            print('thank you for playing.')
            exit()

def next_player():
    # selects next player and take input by calling taking_input func
    global Player1, Player2
    if Player1:
        string = taking_input()
        Player1 = False
        Player2 = True
    elif Player2:
        string = taking_input()
        Player2 = False
        Player1 = True
    return string

def one_player():
    global dif
    #open a file and randomly select a string.
    with open('words.txt') as f:
        file = f.read()
        file_list = file.split('\n') 
        # select one word from list of 11000+ words
        string = random.choice(file_list) 
        if len(string) < 3 or len(string) > 15:
            one_player()  # calling itself
        else:
            word_guess(string, dif)
            play_again_1()  # ask player if they wanna play again

counting_ = 0
def two_player():
    global counting_ 
    global dif
    string = next_player()
    word_guess(string, dif, 2)
    counting_ += 1 
    # if both the player had their chance ask if they wanna play further . if only one player played let other player play two
    if counting_ % 2 == 0:
        res = input('Do u wanna continue playing?\nyes[y]"\t\tno[n]\t\t"cls" - to clear screen\n>> ').strip()
        if res.lower() in ['yes', 'y']:
            two_player()
        elif res.lower() == 'cls':
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')
        else:
            display_score()
            print('thanks for playing.')
            exit()
    else:
        two_player()
        

def word_guess(string, lives = 10, number_of_player = 1):
    np = number_of_player
    word = list(string)     #creating list of that string
    
    #creating '__' underscore list
    fill_word = []
    for i in range(len(string)):
        fill_word.append('__')
    
    print(fill_word)
    print()  # prints next line
    #guessing the answer

    print(f'total lives -  {lives}\t{heart * lives}'.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
    # while player still has life ask for input
    reduce_chance = 3  # this will be reduced if user enters string that contains char other than a word
    while lives > 0:
        guess = input('guess a letter or the whole word:\n>>').strip()
        if guess == '':
            print('empty string not allowed.\n')
            continue

        elif guess.isdigit():
            print('enter a letter or a string.\n')
            reduce_chance -= 1
            if reduce_chance == 0:
                 print(f'your are disqualified for using numbers 3 times, you lose.\
                 \nThe correct word is \'{string}\' \n.')
                 return
            continue
        
        # if player guessed entire word palyer won.
        if guess == string:
            print('you won') if np == 1 else score()
            return
        elif guess in fill_word:
            # if  guessed letter is in fill_word check if count of letter in actual word exceeds in fill_word or not if exceeded deduct life else add that letter to fill_word 
            if string.count(guess) == fill_word.count(guess):
                lives = deduct(lives,fill_word)
            
            elif string.count(guess) > 1:
                ind = string.rfind(guess)
                fill_word.pop(ind)
                fill_word.insert(ind, guess)
                print(fill_word)
            
            else:
                pass
            # if the guessed letters matches all the letters in the string then palyer wins     
            if fill_word == word:
                print('you won') if np == 1 else score()
                return
            # else if guess is in the string then add string to the fill_word at that position    
        elif guess in string:
            ind = string.index(guess)
            fill_word.pop(ind)
            fill_word.insert(ind, guess)
            print(fill_word)
            
            if fill_word == word:
                print('you won') if np == 1 else score()
                return
            # if not in string deduct one life
        else:
            lives = deduct(lives,fill_word)
            
    print(f'your all lives ended, you lose.\nThe correct word is \'{string}\' \nBetter Luck next time.')


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

    