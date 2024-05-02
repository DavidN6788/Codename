from board import Board
from spymaster import Spymaster
from guesser import Guesser
from clue_history import ClueHistory

class GameLogic:
    def __init__(self):
        """
        Initialize the GameLogic for Codenames gameplay
        
        RETURNS(GameLogic): The new constructed object
        """
        self._board = Board()

        # Red team
        self._red_clue_history = ClueHistory('red')
        self._red_spymaster = Spymaster('red', self._board, self._red_clue_history)
        self._red_guesser = Guesser('red', self._board, self._red_clue_history)
        self._red_turns = 0

        # Blue team
        self._blue_clue_history = ClueHistory('blue')
        self._blue_spymaster = Spymaster('blue', self._board, self._blue_clue_history)
        self._blue_guesser = Guesser('blue', self._board, self._blue_clue_history)
        self._blue_turns = 0

        self._scores = self._board.red_blue_left()

    def _add_team_turns(self, team):
        """
        Add to the number of turns the team has played
        
        team(str): the team to add the turns
        """
        if team == 'blue':
            self._blue_turns += 1
        elif team == 'red':
            self._red_turns += 1

    def _get_team_turns(self, team):
        """
        Get the number of turns the team has played

        team(str): the team to add the turns
        """
        if team == 'blue':
            return self._blue_turns
        elif team == 'red':
            return self._red_turns

    def _get_clue_and_number(self, team):
        """
        Get the team's clue and number
        
        team(str): the team to retrieve the clue
        
        RETURNS(Tuple): containing the clue and number
        """
        if team == 'blue':
            return self._blue_spymaster.show_clue_and_number()
        elif team == 'red':
            return self._red_spymaster.show_clue_and_number()

    def _get_guesser(self, team):
        """
        Get the team's Guesser object
        
        team(str): the appointed team
        
        RETURNS(Guesser): the team's Guesser object
        """
        if team == 'blue':
            return self._blue_guesser
        elif team == 'red':
            return self._red_guesser

    def _get_clue_history(self, team):
        """
        Get the team's past clues and intended words
        
        team(str): the appointed team
        
        RETURNS(ClueHistory): the team's ClueHistory object
        """
        if team == 'blue':
            return self._blue_clue_history
        elif team == 'red':
            return self._red_clue_history

    def _get_spymaster(self, team):
        """
        Get the team's Soymaster
        
        team(str): the appointed team
        
        RETURNS(Spymaster): the team's Spymaster object
        """
        if team == 'blue':
            return self._blue_spymaster
        elif team == 'red':
            return self._red_spymaster

    def _print_scores(self):
        """Prints the scores in nicer format"""
        print("Scores: [" + ', '.join([f"'{key}': {value}" for key, value in self._scores.items()]) + "]")

    def _play_round(self, team):
        """
        Recursive function which contain the Codenames logic that
        handles Guesser and Spymaster interactions of a single round.

        team(str): The team which interacts with each other

        RETURNS(tuple): The flag whether assassin or team won and the number of turns taken
        """
        print(f"\n==========\n{team.upper()} TURN\n==========\n")
        # Print board, score, and append turns
        self._print_scores()
        self._board.print_board()

        # Add to how many turns they are on
        self._add_team_turns(team)

        # Start by giving a clue from spymaster and print it
        clue, number = self._get_clue_and_number(team)
        guesses_made = 0
        print(f'{team.capitalize()}: {clue}, {number}')

        # Guesser spymaster interaction
        while True:
            if guesses_made == number:
                print("\n")
                return self._play_round('blue' if team == 'red' else 'red')
            user_input = input(">>> ").split()
            if user_input[0] == "sg":
                print(self._get_guesser(team).suggest_guess())
            elif user_input[0] == "pch":
                self._get_clue_history(team).print_team_clue_history()
            elif user_input[0] == "guess" and len(user_input) > 1 and guesses_made < number:
                guesser = self._get_guesser(team)
                spymaster = self._get_spymaster(team)
                guess = guesser.make_guess(user_input[1])
                guesser.add_to_guessed_words(clue, guess)
                reveal_tag = spymaster.reveal_word(guess)
                round_flag = self._get_round_flag(reveal_tag, spymaster)
                guesses_made += 1
                # Check state of game
                if round_flag == 0:
                    continue
                elif round_flag == 1:
                    print("\n")
                    return self._play_round('blue' if team == 'red' else 'red')
                elif round_flag == 2 or round_flag == 3:
                    # Game lost assassin or Game Win
                    return self._end_game_commands()
            elif user_input == "":
                continue
            else:
                print(f"Invalid {team} team input")

    def _get_round_flag(self, reveal_word, spymaster):
        """
        Alter score or check whether the round or game has ended 
        
        RETURNS(int): 0 - continue team's round,
                      1 - start enemy's round
                      2 - Game has ended
        """
        # Checks whether word was guessed correctly
        if reveal_word == spymaster._team:
            self._scores[spymaster._team] -= 1
            scores = list(self._scores.values())
            # If last word guessed
            if 0 in scores:
                self._print_scores()
                print(f"{spymaster._team} has won!")
                return 3
            else:
                return 0
        elif reveal_word == spymaster._enemy:
            self._scores[spymaster._enemy] -= 1
            return 1
        elif reveal_word == 'neutral':
            return 1
        elif reveal_word == 'assassin':
            print(f"{spymaster._team} has lost!")
            return 2

    def _end_game_commands(self):
        """
        Optional user commands in end game state
        """
        print(f"==========\nGAME HAS ENDED\n==========\n")
        print("blue intended: print blue clue's intended words")
        print("red intended: print red clue's intended words")
        print("psb: prints the spymaster's board")
        print("blue pgw: print blue guessed words")
        print("red pgw: print red guessed words")
        print("end: ends program")
        print("again: Play Codenames again!")
        while(True):
            user_input = input(">>> ").split()
            if user_input[0] == "blue" and user_input[1] == "intended":
                print(self._blue_clue_history.get_clue_intended_words())
            elif user_input[0] == "red" and user_input[1] == "intended":
                print(self._red_clue_history.get_clue_intended_words())
            elif user_input[0] == "blue" and user_input[1] == "pgw":
                self._blue_guesser.print_guessed_words()
            elif user_input[0] == "red" and user_input[1] == "pgw":
                self._red_guesser.print_guessed_words()
            elif user_input[0] == "psb":
                self._board.print_spymaster_board()
            elif user_input[0] == "end":
                break
            elif user_input[0] == "again":
                game_logic = GameLogic()
                game_logic.play_game()
            else:
                print(f"Invalid input for end game")

    def play_game(self):
        """
        Main CODENAMES gameplay
        """
        print("_______________________________")
        print("------ Starting Codenames------")
        print("_______________________________")
        print("\n")

        print("-----OPTIONS TO INPUT-----")
        print("pgb: prints the guesser's board")
        print("guess (your word): make a guess on the board")
        print("sg: give suggestions for current clue and number")
        print("pch: print past clues given")
        print("\n")

        # Blue team starts
        self._play_round('blue')

    def automate_game(self, team):
        """
        Automates a single Codename gameplay where the spymaster 
        and guesser autonomously interacts
        
        team(str): The current team in play
        
        RETURNS(Tuple/automate_game()): Either calls itself recursively or 
        a tuple containing:
        - team
        - round flag
        - # of team turns
        - team clue intended words
        - team guessed words
        """
        print(f"\n==========\n{team.upper()} TURN\n==========\n")
        # Start by giving clue
        clue, number = self._get_clue_and_number(team)
        # Add to how many turns they are on
        self._add_team_turns(team)
        guesses_made = 0

        # Start playing by itself
        while(True):
            # Check if number of guesses made equals the intended clue number
            if guesses_made == number:
                return self.automate_game('blue' if team == 'red' else 'red')

            print("Suggesting clues")
            # Guesser automates guessed words
            suggested_clues = self._get_guesser(team).suggest_guess()
            guesser = self._get_guesser(team)
            spymaster = self._get_spymaster(team)

             # Input all the guess clue suggested
            for word in suggested_clues:
                guess = guesser.make_guess(word)
                guesser.add_to_guessed_words(clue, guess)
                reveal_tag = spymaster.reveal_word(guess)
                round_flag = self._get_round_flag(reveal_tag, spymaster)
                guesses_made += 1
                if round_flag == 0:
                    continue
                elif round_flag == 1:
                    print("\n")
                    return self.automate_game('blue' if team == 'red' else 'red')
                elif round_flag == 2 or round_flag == 3:
                    # Game lost assassin
                    team_clue_history = self._get_clue_history(team)
                    team_guesser = self._get_guesser(team)
                    return team, round_flag, self._get_team_turns(team), team_clue_history.get_clue_intended_words(), team_guesser.get_guessed_words()

    def automate_single_guess_round(self, team):
        """
        Automates a single Codename guessing round where the spymaster 
        and guesser autonomously interacts.
        
        team(str): The current team in play
        
        RETURNS(Tuple): Either calls itself recursively or 
        a tuple containing:
        - team
        - round flag
        - # of team turns
        - team clue intended words
        - team guessed words
        """
        print(f"\n==========\n{team.upper()} TURN\n==========\n")
        # Start by giving clue
        clue, number = self._get_clue_and_number(team)
        # Add to how many turns they are on
        self._add_team_turns(team)
        guesses_made = 0

        print("Suggesting clues")
        # Guesser automates guessed words
        suggested_clues = self._get_guesser(team).suggest_guess()
        guesser = self._get_guesser(team)
        spymaster = self._get_spymaster(team)

        # Input all the guess clue suggested
        for word in suggested_clues:
            guess = guesser.make_guess(word)
            guesser.add_to_guessed_words(clue, guess)
            reveal_tag = spymaster.reveal_word(guess)
            round_flag = self._get_round_flag(reveal_tag, spymaster)
            guesses_made += 1
            team_clue_history = self._get_clue_history(team)
            team_guesser = self._get_guesser(team)
            if guesses_made == number:
                return team, round_flag, self._get_team_turns(team), team_clue_history.get_clue_intended_words(), team_guesser.get_guessed_words()

if __name__ == "__main__":
    game_logic = GameLogic()
    game_logic.play_game()
