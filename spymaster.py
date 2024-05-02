import re

class Spymaster():
    def __init__(self, team, board, clue_history):
        """
        Initialize the Spymaster object.

        team(str): the team the spymaster is assigned
        board(Board): the Board object
        clue_history: the ClueHistory object

        RETURNS(Spymaster): The newly constructed object
        """
        self._board = board
        self._clue_history = clue_history
        self._team = 'red' if team == 'red' else 'blue'
        self._enemy = 'blue' if team == 'red' else 'red'

    def show_clue_and_number(self):
        """ 
        Check which algorithm and embedding model to use to generate clue and number

        RETURNS(Tuple): A tuple containing the best clue (str) and intended number (int)
        """
        print("Generating clue...\n")

        embedding_model = self._board._embedding_model
        return self._heuristic_algorithm(embedding_model)

    def _heuristic_algorithm(self, embedding_model):
        team_words = self._board.get_tag_words().get(self._team)
        bad_words = self._board.get_tag_words().get(self._enemy) + self._board.get_tag_words().get('neutral') + self._board.get_tag_words().get('assassin')
        top_num = self._board._config['hyperparameters']['topn']
        embedding = self._board._embedding
        word_vocab = []

        # Get most similar words to team words as vocabulary
        for team_word in team_words:
            if team_word == "------":
                continue
            if embedding == "word2vec":
                most_similar = embedding_model.most_similar_words(team_word, topn=top_num)
                for most_similar_word in most_similar:
                    curr_word = most_similar_word.lower()
                    if curr_word not in self._board._embedding_model.get_model():
                        continue
                    # Exclude words that include base forms
                    if curr_word in team_words or team_word in curr_word:
                        continue
                    # Check if word is a singular word and not already in vocab
                    if re.match(r"^\w+$", curr_word) and curr_word not in word_vocab and "_" not in curr_word:
                        word_vocab.append(curr_word)
            elif embedding == "sense2vec":
                _, most_similar = embedding_model.most_similar_words(team_word, topn=top_num)
                for most_similar_word in most_similar:
                    curr_word = most_similar_word.split('|')[0]
                    # Exclude words that include base forms
                    if curr_word in team_words or team_word in curr_word:
                        continue
                    else:
                        word_vocab.append(most_similar_word)
        
        # Heuristic decision algorithm
        best_clue = None
        intended_number = 0
        intended_word = []
        best_score = float('-inf')
        similar_to_team_scores = []
        similar_to_bad_scores = []
        a = 0
        for word in word_vocab:
            # # Check if clue already exists
            if word in self._clue_history._clue_history.keys():
                continue

            # Calculate the cosine similarity between word in vocab and team words            
            try:
                similar_to_team_scores = [embedding_model.similarity(word, team_word) 
                                        for team_word in team_words]
                similar_to_bad_scores = [embedding_model.similarity(word, bad_word) 
                                        for bad_word in bad_words]
            except TypeError:
                pass
            similarity_score = sum(similar_to_team_scores) - sum(similar_to_bad_scores)

            # Keep track of best score and clue
            if similarity_score > best_score:
                best_clue = word
                best_score = similarity_score
        intended_number, intended_word = self._generate_intended_number(team_words, best_clue, embedding_model)
        self._clue_history.add_to_history(best_clue, intended_word)
        return best_clue, intended_number

    def _generate_intended_number(self, team_words, best_clue, embedding_model):
        """
        This function generates the best intended number of words on the board given a clue
        and appends on those intended words into the clue history
        
        team_words(list): all the words of the spymaster's team
        best_clue(str): The best clue generated which is similar to all the team words
        embedding_model: The word embedding model used for similarity calculations
        
        RETURNS(int, list): The best intended number to the team words given a clue and intended words  
        """
        cosine_sim_difference = self._board._config['hyperparameters']['cosine_sim_difference']
        max_intended_number = 3
        intended_number = 1
        most_similar = {}
        intended_word = []
        # Calculate how similar the scores are to the best clue in descending order
        for team_word in team_words:
            if team_word == "------":
                continue
            similarity_score = embedding_model.similarity(best_clue, team_word)
            most_similar[team_word] = similarity_score
        sorted_most_similar = sorted(most_similar.items(), key=lambda x:x[1], reverse=True)

        # If only one word left on the board
        if len(sorted_most_similar) == 1:
            intended_word.append(sorted_most_similar[0][0])
        else:
            # Loop through the 3 highest word scores
            for i in range(len(sorted_most_similar[:max_intended_number]) - 1):
                # If the difference between each consecutive pairs is less than the cosine sim
                # difference append to clue history and the intended number
                if (sorted_most_similar[i][1] - sorted_most_similar[i+1][1]) < cosine_sim_difference:
                    intended_number += 1
                    intended_word.append(sorted_most_similar[i][0])
                    intended_word.append(sorted_most_similar[i+1][0])
                else:
                    intended_word.append(sorted_most_similar[i][0])
                    break

        return intended_number, list(set(intended_word))

    def reveal_word(self, word):
        """
        Reveals the tag of the word given a word from the guesser

        word(str): The word guessed by the guesser.
        RETURNS(str|None): The tag of the word or None if word is not on board
        """
        # Check if word is on codenames board
        if word in self._board.get_board_words():
            for key, value in self._board.get_tag_words().items():
                # Replace word with blank value "------"
                if word in value:
                    replace_index = value.index(word)
                    value[replace_index] = "------"
                    # Check which tag the word belongs to
                    if key == self._team:
                        print(f"You have found your {self._team} word!")
                        return self._team
                    elif key == self._enemy:
                        print(f"You have found the enemy's {self._enemy} word")
                        return self._enemy
                    elif key == 'neutral':
                        print("You have found a neutral word")
                        return 'neutral'
                    elif key == 'assassin':
                        print("You have found an assassin word")
                        return 'assassin'
        else:
            print("Word is not on board")
            return
