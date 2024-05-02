from collections import defaultdict

class Guesser():
    def __init__(self, team, board, clue_history):
        """
        Initialize the Guesser Object.

        board(Board): the constructed Board object
        clue_history(ClueHistory): the constructed ClueHistory Object

        RETURNS(Guesser): the newly constructed object
        """
        self._team = team
        self._board = board
        self._history = clue_history
        self._guessed_words = defaultdict(list)

    def suggest_guess(self):
        """ 
        Check which algorithm and embedding model to use to suggest guess

        RETURNS(List): A list of words most similar to the latest clue
        """
        return self._heuristic_algorithm()


    def _heuristic_algorithm(self):
        """
        A heuristic algorithm which finds out which words were intended
        given the spymaster's clue

        RETURN(list):  A list of the words most similar to the clue
        """
        last_clue = self._history.get_last_clue()
        # Get intended number of words
        clue_number = len(self._history._clue_history[last_clue])
        word_score = {}

        # Iterate through each word on the board
        for word in self._board.get_current_words():
            if word == "------":
                continue
            sim_score = self._board._embedding_model.similarity(last_clue, word)
            word_score[word] = sim_score
        # Sort the words with the highest similarity
        sorted_word_score = dict(sorted(word_score.items(), key=lambda item: item[1], reverse=True))
        most_similar_words = list(sorted_word_score.keys())
        return most_similar_words[:clue_number]

    def make_guess(self, word):
        """
        Choose a word as a guess

        word(str): The word chosen

        RETURNS(str): The word chosen for the guess
        """
        return word

    def add_to_guessed_words(self, clue, word):
        """
        Add the Guesser's guesses to the default dict.

        clue(str): the clue that was provided to the guesser
        guess(str): the guesser guess given the clue
        """
        self._guessed_words[clue].append(word)

    def get_guessed_words(self):
        """
        Convert guessed words from defaultdict to dictionary

        RETURNS(dict): the guessed words converted to dict
        """
        return dict(self._guessed_words)

    def print_guessed_words(self):
        """
        Print all the guessed words
        """
        guessed_words = dict(self._guessed_words)
        for key, value in guessed_words.items():
            print(f'{key}: {value}')
