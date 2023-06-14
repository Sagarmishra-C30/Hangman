#guess the word. with lives u have
import random
import re
import os
import getpass
import sys
import time
from datetime import datetime, timedelta

if sys.stdout.encoding is None:
    # Set the default encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

#global useful variables
heart = '\u2665'  # unicode char for heart
Player1 = True
Player2 = False
score1, score2 = 0, 0
num_players = 1
dif = None
word_length = 0
player1_name = None
player2_name = None
hint_counter = 3  # Set the initial number of hints

difficulties = {
    'easy': {'word_length': (3, 10), 'difficulty': 10},
    'normal': {'word_length': (6, 12), 'difficulty': 7},
    'hard': {'word_length': (10, 20), 'difficulty': 5}
}

# Define the category options as a dictionary
categories = {
    "0": {
        "name": "Random",
        "file": "words.txt"
    },
    "1": {
        "name": "Animals",
        "file": "animals.txt"
    },
    "2": {
        "name": "Countries",
        "file": "countries.txt"
    },
    "3": {
        "name": "Movies",
        "file": "movies.txt"
    },
    "4": {
        "name": "Fish",
        "file": "fish.txt"
    },
    "5": {
        "name": "Birds",
        "file": "birds.txt"
    },
    "6": {
        "name": "Animes",
        "file": "animes.txt"
    },
}

# Define the time limit (in seconds) for the round
round_time_limit = 180  # 3 minutes

# Define the time limit (in seconds) for each guess
time_limit = 15


hang = r'''
 ___________.._______      You are on a roll, my friend! 
| .__________))______|                 How do you do it?
| | / /      ||
| |/ /       ||
| | /        ||.-''.
| |/         |/  _  \
| |          ||  `/,|  Everytime you play Hangman,
| |          (\\`_.'    a stickman family is left 
| |         .-`--'.              without a father.
| |        /Y . . Y\
| |       // |   | \\
| |      //  | . |  \\        Congrants on your impressive
| |    (')   |   |  (`)        stickman extermination skills!
| |          ||'||             
| |          || ||        
| |          || ||        You've got some serious talent for turning
| |          || ||         innocent stickman into twisted stick pretzels
| |         / | | \
""""""""""|_`-' `-' 
|"|"""""""\ \         
| |        \ \        We should consider hiring you as their official terminator.
: :         \ \       
. .          `'      

'''
fireworks = r"""
                        We are celebrating your victory
⠀                                       .
              . .                     -:-             .  .  .
            .'.:,'.        .  .  .     ' .           . \ | / .
            .'.;.`.       ._. ! ._.       \          .__\:/__.
             `,:.'         ._\!/_.                     .';`.      . ' .
             ,'             . ! .        ,.,      ..======..       .:.
            ,                 .         ._!_.     ||::: : | .        ',
     .====.,                  .           ;  .~.===: : : :|   ..===.
     |.::'||      .=====.,    ..=======.~,   |"|: :|::::::|   ||:::|=====|
  ___| :::|!__.,  |:::::|!_,   |: :: ::|"|l_l|"|:: |:;;:::|___!| ::|: : :|
 |: :|::: |:: |!__|; :: |: |===::: :: :|"||_||"| : |: :: :|: : |:: |:::::|
 |:::| _::|: :|:::|:===:|::|:::|:===F=:|"!/|\!"|::F|:====:|::_:|: :|::__:|
 !_[]![_]_!_[]![]_!_[__]![]![_]![_][I_]!//_:_\\![]I![_][_]!_[_]![]_!_[__]!
 -----------------------------------"---''''```---"-----------------------
 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ |= _ _:_ _ =| _ _ _ _ _ _ _ _ _ _ _ _
                                     |=    :    =|                Valkyrie
_____________________________________L___________J________________________
--------------------------------------------------------------------------
"""

cheers = r'''
             .-"""-.
            /       \
            \       /
     .-"""-.-`.-.-.<  _
    /      _,-\ O_O-_/ )  ~champagne, monsieur?
    \     / ,  `   . `|
     '-..-| \-.,__~ ~ /          .,
           \ `-.__/  /          /"/
          / `-.__.-\`-._    ,",' ;
         / /|    ___\-._`-.; /  ./-.  
        ( ( |.-"`   `'\ '-( /  //.-' congrats on winning!.
         \ \/    {}{}  |   /-. /.-'   You saved a hangman from dying today!.
          \|           /   '..'          aren't you a hero?
           \        , /
           ( __`;-;'__`)
           `//'`   `||`
          _//       ||
  .-"-._,(__)     .(__).-""-.
 /          \    /           \
 \          /    \           /
  `'-------`      `--------'`
'''

win = fireworks + '\n\n' + cheers

game_title_1 = r"""
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/                       
"""

game_title_2 = r"""
#     #    #    #     #  #####  #     #    #    #     #     #####     #    #     # ####### 
#     #   # #   ##    # #     # ##   ##   # #   ##    #    #     #   # #   ##   ## #       
#     #  #   #  # #   # #       # # # #  #   #  # #   #    #        #   #  # # # # #       
####### #     # #  #  # #  #### #  #  # #     # #  #  #    #  #### #     # #  #  # #####   
#     # ####### #   # # #     # #     # ####### #   # #    #     # ####### #     # #       
#     # #     # #    ## #     # #     # #     # #    ##    #     # #     # #     # #       
#     # #     # #     #  #####  #     # #     # #     #     #####  #     # #     # #######
"""




# Function to get user input within the time limit
def get_user_input():
    print('Guess a letter or the whole word:')
    start_time = time.time()  # Get the current time
    user_input = input(">> ").strip().lower()
    elapsed_time = time.time() - start_time  # Calculate the elapsed time

    # Check if the time limit has been exceeded
    if elapsed_time > time_limit:
        print("Time's up!")
        return None

    return user_input

# Function to check if the round time limit has been exceeded
def is_round_time_up(start_time):
    elapsed_time = time.time() - start_time  # Calculate the elapsed time
    return elapsed_time > round_time_limit

# Function to format the time in MM:SS format
def format_time(seconds):
    time_str = ""
    if seconds // 3600 > 0:
        hours = seconds // 3600
        time_str += f"{hours} hour(s) "
        seconds %= 3600
    if seconds // 60 > 0:
        minutes = seconds // 60
        time_str += f"{minutes} minute(s) "
        seconds %= 60
    time_str += f"{seconds:.2f} second(s)"
    return time_str
    

def display_categories():
    # Display available categories
    print("Available categories:")
    for key, category in categories.items():
        print(f"{key}. {category['name']}")
    print()

def select_category():
    while True:
        display_categories()
        category_choice = input("Select a category (enter the corresponding number): ")
        if category_choice in categories:
            print(f"Category selected -> {categories[category_choice]['name'].upper()}\n")
            return category_choice
        else:
            print("Invalid category choice. Defaulting to 0 - Random.\nCategory selected -> RANDOM\n")
            return "0"

def load_words_from_file(file_path):
    with open(f"words/{file_path}") as f:
        word_list = [word.strip() for word in f if word_length[0] <= len(word.strip()) <= word_length[1]]
    return word_list

def provide_hint(word, fill_word):
    global hint_counter

    # Check if there are remaining hints
    if hint_counter > 0:
        hint_counter -= 1  # Decrease the hint counter by 1
        indices = [index for index, letter in enumerate(word) if fill_word[index] == "__"]
        random_index = random.choice(indices)  # Select a random hidden letter index
        fill_word[random_index] = word[random_index]  # Reveal the letter at the selected index
        print("Hint: One letter has been revealed.\n")
        print(" ".join(fill_word))  # Display the updated fill_word
    else:
        print("Sorry, no more hints available.")


def difficulty():
    # Set difficulty level
    difficulty = input('Choose difficulty level:\na) Easy[e]\t\tb) Normal[n]\t\tc) Hard[h]\n').strip()
    if difficulty.lower() in ['easy', 'e', '1']:
        print("difficulty selected to EASY")
        return difficulties['easy']['word_length'], difficulties['easy']['difficulty']
    if difficulty.lower() in ['hard', 'h', '3']:
        print("difficulty selected to HARD")
        return difficulties['hard']['word_length'], difficulties['hard']['difficulty']
    elif difficulty.lower() in ['normal', 'n', '2']:
        print("difficulty selected to NORMAL")
        return difficulties['normal']['word_length'], difficulties['normal']['difficulty']
    else:
        print('Invalid choice. Defaulting to easy difficulty.\n"difficulty selected to EASY"')
        return difficulties['easy']['word_length'], difficulties['easy']['difficulty']

def score():
    # Score of player
    global Player1, Player2, score1, score2
    correct_guess_str = "{} You guessed correctly!!!\n"
    # print(win)
    if Player1:
        score1 += 1
        print(correct_guess_str.format(player1_name))
    elif Player2:
        score2 += 1
        print(correct_guess_str.format(player2_name))

def display_score():
    # Display score, winner, and loser
    if score1 > score2:
        print(win)
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\n\n' +
        f'{"*"*20}  Winner is {player1_name}  {"*"*20}'.center(100) + '\n')
    elif score1 < score2:
        print(win)
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\n\n' + 
        f'{"*"*20}  Winner is {player2_name}  {"*"*20}'.center(100) + '\n')
    else:
        print(f'{player1_name} score = {score1}\t\t{player2_name} score = {score2}\n\n' +
        f'{"*"*20}  Draw  {"*"*20}'.center(100) + '\n')
        print("You both need more practice!\nStop playing and study!\or are you both ready to challenge another round?")
    

def deduct(lives):
    lives -= 1
    # Deduct player's life if guessed wrong
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
    global word_length, dif
    # Ask player whether to play again or not
    while True:
        response = input('\nDo you want to play again?\nType - a) Yes[y]\t\tb) No\t\t"cls" - to clear screen \
        \t\t"reset" - to reset difficulty\n>>')
        if response.lower() == 'yes' or response.lower() == 'y':
            one_player()
        elif response.lower() == 'cls':
            if os.name == "nt":
                os.system('cls')
            else:
                os.system('clear')
        elif response.lower() == 'reset':
            word_length, dif = difficulty()
            print(f'You have total - {dif} lives\t{heart * dif}\n'.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
            one_player()
        else:
            print('\nThanks for playing\t\t' + game_title_1)
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
    global word_length, dif, num_players, player1_name, player2_name
    num_players = 1
    category_choice = select_category()

    # Get the selected category details
    selected_category = categories[category_choice]
    category_name = selected_category["name"]
    file_path = selected_category["file"]

    # Load words from the selected category file
    word_list = load_words_from_file(file_path)
    
    # Select one word from the list of 11000+ words
    string = (random.choice(word_list)).lower()
    if len(string) < 3 or len(string) > 15:
        one_player()
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
            print('\nThanks for playing\t\t' + game_title_1)
            exit()
    else:
        two_player()
        

def create_fill_word(string):
    fill_word = []
    for char in string:
        if char == ' ':
            fill_word.append(' ')
        else:
            fill_word.append('__')
    return fill_word

def process_guess(guess, string, fill_word, lives):
    if guess == '' or guess == ' ':
        print('Empty string not allowed.\n')
        return lives

    if guess.isdigit():
        print('Enter a letter or a string.\n')
        return deduct(lives)

    if guess in string:
        for index, letter in enumerate(string):
            if letter == guess:
                fill_word[index] = guess
        return lives

    return deduct(lives)

def is_word_complete(fill_word, word):
    return fill_word == word

def word_guess(string, lives=10, number_of_player=1):
    num_players = number_of_player
    word = list(string)
    fill_word = create_fill_word(string)

    print(' '.join(fill_word))
    print()
    guessed_letters = []
    start_time = time.time()  # Start the timer for the round
    
    while lives > 0:
        # Calculate the remaining time
        guess = get_user_input()
        
        # Check if the round time limit has been exceeded
        if is_round_time_up(start_time):
            print("\nROUND TIME'S UP!")
            break
            
        if guess is None:
            # Time's up, handle accordingly (e.g., deduct a life, end the game, etc.)
            print("You took too long to guess!")
            lives = deduct(lives)
        elif guess.lower() == "hint":   # Check if the player wants a hint
            provide_hint(word, fill_word)
            print('_'*50 + '\n')
            continue
        elif guess in guessed_letters:
            print("You already guessed that letter.\n")
        else:
            lives = process_guess(guess, string, fill_word, lives)
            if guess == string:
                print(f'You won\n\n{win}') if num_players == 1 else score()
                return
            elif is_word_complete(fill_word, word):
                print(f'You won\n\n{win}') if num_players == 1 else score()
                return
        
        guessed_letters.append(guess)
        # Display the ticking timer to the user
        elapsed_time = time.time() - start_time
        remaining_time = round_time_limit - elapsed_time
        print(f"Time remaining: {format_time(remaining_time)}")
        print(' '.join(fill_word))
        print(f'Total lives: {lives}\t{heart * lives}\n'.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        print('_'*50 + '\n')

    if num_players == 1:
        print(f'Your lives are over. You lose.\nThe correct word is \'{string}\'.\nBetter luck next time.\n\n')
        print(hang)
    else:
        if Player1:
            print(f"{player1_name}, your guess was wrong.\nThe correct word is '{string}'\n")
            print(hang)
        else:
            print(f"{player2_name}, your guess was wrong.\nThe correct word is '{string}'\n")
            print(hang)


def main():
    global word_length, dif, player1_name, player2_name
    print(game_title_2)
    print('\n' + f'{"*"*10}  welcome to Hangman Game  {"*"*10}'.center(100) + '\n\n')
    play = input('"1"- for 1-Player game\t\t"2" for 2-Player game\t\t"exit" - to exit the game\n>> ').strip()
    if play == '1':
        word_length, dif = difficulty()
        print(f'You have total - {dif} lives\t{heart * dif}\n'.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        print(f"[[ You have ***{hint_counter} hints*** available per round.\nTo use hints simply type -> 'hint' and hit enter.]]\n")
        one_player()
    elif play == '2':
        player1_name = input("enter your name player 1:\n>> ")
        player2_name = input("enter your name player 2:\n>> ")
        _, dif = difficulty()
        print(f'You both have total - {dif} lives\t{heart * dif}\n'.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        two_player()
    else:
        print("Please select correct option")
        exit()

if __name__ == "__main__":
    main()

    