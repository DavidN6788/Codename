from main import GameLogic
import random
import yaml

def load_config(config_file):
    """Load and parse the config yaml file.

    config_file: The path to the config file
    RETURNS (Dict): The config as key value pairs
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def average_min_num_of_turns(num_of_games):
    """
    Autonomously plays multiple Codenames games and calculates the average number of 
    turns, the minimum number of turns, and how many games were assassins

    RETURNS(Tuple): Average turns, minimum turns, assassin games
    """
    total_turns = []
    assassin_game = 0
    for i in range(num_of_games):
        print(f"\n====== GAME {i + 1} ======\n")
        gameLogic = GameLogic()
        try:    
            _, flag, turns,_ ,_ = gameLogic.automate_game("blue")
        except TypeError:
            print("Failed game")
            continue
        if flag == 3:
            total_turns.append(turns)
        elif flag == 2:
            assassin_game += 1
            continue
    if total_turns:
        average_turns = sum(total_turns) / len(total_turns)
        min_turns = min(total_turns)
    else:
        average_turns = 0
        min_turns = 0
    return average_turns, min_turns, assassin_game

def correct_intended_words(num_of_games):
    """
    Autonomously plays multiple Codenames games and calculates total clues given, correct guessed words,
    and how many games were assassins

    RETURNS(Tuple): Total clues, correct guessed words, assassin games
    """
    total_clues = 0
    correct_guessed_words = 0
    assassin_game = 0
    for i in range(num_of_games):
        print(f"\n====== GAME {i + 1} ======\n")
        gameLogic = GameLogic()
        try:
            _, flag, _, intended_words, guessed_words = gameLogic.automate_game("blue")
        except TypeError:
            print("Failed game")
            continue
        if flag == 2:
            assassin_game += 1
            continue
        elif flag == 3:
            for key in intended_words:
                if key in guessed_words:
                    correct_guessed_words  += sum(1 for word in intended_words[key] if word in guessed_words[key])
                    total_clues += len(intended_words[key])
    return total_clues, correct_guessed_words, assassin_game

def correct_intended_words_single_round(num_of_games):
    """
    Autonomously a single Codenames round and calculates total clues given, correct guessed words,
    and how many games were assassins

    RETURNS(Tuple): Total clues, correct guessed words, assassin games
    """
    total_clues = 0
    correct_guessed_words = 0
    assassin_game = 0
    for i in range(num_of_games):
        print(f"\n====== GAME {i + 1} ======\n")
        gameLogic = GameLogic()
        try:
            _, flag, _, intended_words, guessed_words = gameLogic.automate_single_guess_round("blue")
        except TypeError:
            print("Failed game")
            continue
        # Skip for assassin
        if flag == 2:
            assassin_game += 1
            continue
        for key in intended_words:
            if key in guessed_words:
                correct_guessed_words  += sum(1 for word in intended_words[key] if word in guessed_words[key])
                total_clues += len(intended_words[key])
    return total_clues, correct_guessed_words, assassin_game

"""
EXPERIMENT DATA
"""
# Set random seed
random.seed(50)

# Config
config = load_config('config.yaml')

embedding_model = config['parameters']['embedding_model']
vocab_size = config['hyperparameters']['vocab_size']
cos_difference = config['hyperparameters']['cosine_sim_difference']
topn = config['hyperparameters']['topn']
num_of_games = config['experiment_params']['num_of_games']

print("\n")
print("Embedding Model:", embedding_model)
print("Vocabulary Size:", vocab_size)
print("Cosine similarity difference:", cos_difference)
print("Top N:", topn)
print("Num of games:", num_of_games)
print("\n")

# Play normal Codenames games
average_turns, min_turns, assassin_games = average_min_num_of_turns(num_of_games)
print(f'\nAverage turns: {average_turns}, Minimum turns: {min_turns}, Failed games: {assassin_games}\n')

# Play Codenames games for intended words
total_clues, correct_guessed_words, total_assassin_games = correct_intended_words(num_of_games)
print(f'\nTotal clues: {total_clues}, Correct guessed words: {correct_guessed_words}, Failed games: {total_assassin_games}\n')

# Play Codenames games for single round
single_total_clues, single_correct_guessed_words, single_assassin_games = correct_intended_words_single_round(num_of_games)
print(f'\nTotal clues (Single Round): {total_clues}, Correct guessed words: {correct_guessed_words}, Failed games: {assassin_games}\n')

average_turns_list = [average_turns, min_turns, assassin_games]
single_game_clues_list = [total_clues, correct_guessed_words, assassin_games]
single_round_clues_list = [single_total_clues, single_correct_guessed_words, single_assassin_games]
print(average_turns_list)
print(single_game_clues_list)
print(single_round_clues_list)