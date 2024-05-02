from embedding_model import EmbeddingModel
from tabulate import tabulate
import random
import numpy as np
import copy

class Board():
    def __init__(self):
        self._embedding_model = EmbeddingModel()
        self._config = self._embedding_model._config
        self._file_path = self._config['model_paths']['codename_words']['file_path']
        self._embedding = self._config['parameters']['embedding_model']
        self._board_words = self._set_board_words(self._file_path)
        self._tag_words = self._set_tag_words()
        self._tag_words_copy = copy.deepcopy(self._tag_words)

    def _set_board_words(self, file_path):
        """
        Retrieves all the words used for codenames and check whether
        these words exists in embedding model. Then it randomly samples
        25 of those words for the board
        
        file_path(str): The path to the words.txt file which contains all
        codename words
        
        RETURNS(list): Sampled list of 25 words used for codenames board
        """
        print("Creating board...")
        with open(file_path, 'r') as file:
            # Get all the words from codenames word list
            file_words = file.read().split()
        if self._embedding == 'word2vec':
            # Check whether file_words exists in model
            codename_words = list(set([word for word in file_words if word in self._embedding_model.get_model()]))
        elif self._embedding == 'sense2vec':
            # Get best sense for file words
            file_words_sense = []
            # Handle keys that are not present in model
            for word in file_words:
                try:
                    best_sense = self._embedding_model.get_model().get_best_sense(word)
                    file_words_sense.append(best_sense)
                except KeyError:
                    continue
            codename_words = list(set(file_words_sense))
        board_words = random.sample(codename_words, 25)
        random.shuffle(board_words)
        return board_words

    def _set_tag_words(self):
        """
        Assign tags (red, blue, neutral, and assassin) to the words on the board

        RETURNS(dict): A dictionary with tag-word as key-value pairs
        """
        # Get all the words on the board and shuffle them
        words = self._board_words
        random.shuffle(words)

        # Assign tags to codename words
        board = {}
        board['red'] = words[:8]
        board['blue'] = words[8:17]
        board['neutral'] = words[18:25]
        board['assassin'] = [words[17]]
        return board

    def get_board_words(self):
        """
        Get _board_words attribute

        RETURNS(list): the list of all words used for board
        """
        return self._board_words

    def get_tag_words(self):
        """
        Get _tag_words attribute

        RETURNS(dict): dictionary containing the tags of respective words
        """
        return self._tag_words

    def get_current_words(self):
        """
        Get _current_words

        RETURNS(list): list of current words on the board
        """
        self._current_words = [word for words in self.get_tag_words().values() for word in words]
        return self._current_words

    def print_board(self):
        """
        Prints the guesser board in a nice format
        """
        words = [word for _, value in self._tag_words.items() for word in value]

        words = np.array(words).reshape(5, 5).copy()
        table = tabulate(words, tablefmt="fancy_grid")
        print(table)

    def print_spymaster_board(self):
        """
        Print the spymaster board showing tags and words
        """
        for key, value in self._tag_words_copy.items():
            print(f'{key}: {value}')

    def red_blue_left(self):
        """
        Retrieve how many red and blue words are left on the board

        RETURN(dict): The number of reds and blues left
        """
        remaining = {}
        reds_left = sum(1 for words in self._tag_words.get("red", []) if words != "------")
        blues_left = sum(1 for words in self._tag_words.get("blue", []) if words != "------")
        remaining['red'] = reds_left
        remaining['blue'] = blues_left
        return remaining
