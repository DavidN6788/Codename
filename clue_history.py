from collections import defaultdict

class ClueHistory():
    def __init__(self, team):
        self._clue_history = defaultdict(list)
        self._team = team

    def add_to_history(self, clue, intended_words):
        """
        Add clue and the intended words to clue history

        clue(str): the clue given by a spymaster
        intended_words(list): a list of the words intended by the clue
        """
        self._clue_history[clue].extend(intended_words)

    def get_last_clue(self):
        """
        Get the latest clue given by the spymaster

        RETURNS(str): The latest clue
        """
        return list(self._clue_history.keys())[-1]

    def get_clue_intended_words(self):
        """
        Gets the intended words with past clues

        RETURNS(Tuple): The clue and intended words
        """
        return dict(self._clue_history.items())

    def print_team_clue_history(self):
        """
        Print the team's past clues

        RETURNS(list): The clues
        """
        team_clues = list(self._clue_history.keys()) 
        for clue in team_clues:
            print(clue)
        return team_clues
