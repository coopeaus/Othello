# Author: Austin Cooper
# GitHub username: amcooper181

from othello_class import *
from minimax import *
import random


class NewGame:
    """
    Represent an individual game of Othello
    """
    def __init__(self):
        self._player_1 = None
        self._player_2 = None
        self._game = Othello()
        self._difficulty = None
        self._show_available = None

    def create_players(self):
        """Create the objects representing the player(s) playing Othello."""

        self._player_1 = Player(input("Player 1, please enter your name: "), "black")
        opponent_option = input(f"Hello, {self._player_1.get_name()}, would you like to play against the computer "
                                f"or a human opponent? Enter '1' for computer or '2' for human: ")
        valid_entry = False
        while not valid_entry:
            if opponent_option == "1":
                self._player_2 = Player("PC", "white")
                valid_entry = True
            elif opponent_option == "2":
                self._player_2 = Player(input("\nPlayer 2, please enter your name: "), "white")
                valid_entry = True
            else:
                opponent_option = input("\nInvalid entry! Please enter '1' for computer or '2' for human: ")
        self._game.add_player(self._player_1)
        self._game.add_player(self._player_2)

    def choose_computer_difficulty(self):
        """Choose if the computer will choose randomly or aggressively"""
        self._difficulty = input("\nDifficulty: Would you like the computer to behave randomly, or aggressively? "
                                 "Enter 'random' for random tile choices or 'aggressive' for aggressive choices: ")

        valid_entry = False
        while not valid_entry:
            if self._difficulty == "random" or "aggressive":
                valid_entry = True
            else:
                self._difficulty = input("Invalid entry! Please enter 'random' or 'aggressive': ")

    def available_tiles(self):
        """Choose if the available tiles for each player move will be shown"""
        show_avail = input("\nWould you like to see available tiles for each player turn? Enter 'y' for yes "
                           "or 'n' for no: ")
        valid_entry = False
        while not valid_entry:
            if show_avail == "y":
                self._show_available = True
                input("Available tiles will be denoted by the character 'A'. Enter to continue...")
                valid_entry = True
            elif show_avail == "n":
                self._show_available = False
                valid_entry = True
            else:
                show_avail = input("\nInvalid entry! Please enter 'y' or 'n': ")

    def _get_player_move(self, player_color):
        """Prompt player for a move"""
        if player_color == 'black':
            piece = 'X'
        else:
            piece = 'O'

        move_control = 0
        while move_control == 0:
            try:
                row = int(input("Please enter the row of the piece you would like to play: "))
                col = int(input("Please enter the column of the piece you would like to play: "))
                if (row, col) in self._game.return_available_positions(player_color):
                    return row, col
                else:
                    print("Invalid move! Please try again.")
                    print(f"Available moves: {self._game.return_available_positions(player_color)}")
            except ValueError:
                print("Invalid entry! Please enter a valid integer.")

    def display_board(self):
        """Display the board with formatting"""
        print("\n")
        self._game.print_board()
        print("\n")

    def _move_status(self):
        """
        Determine if there are no more available moves, meaning the game is ended. Helper
        function for game_status()
        """
        black_remaining = len(self._game.return_available_positions('black'))
        white_remaining = len(self._game.return_available_positions('white'))
        if black_remaining == 0 and white_remaining == 0:
            return True, True
        elif black_remaining == 0:
            return True, False
        elif white_remaining == 0:
            return False, True
        return False, False

    def game_status(self, player_color):
        """
        Determine if there are no more available moves, meaning the game is ended.
        """
        black, white = self._move_status()
        if black and white:
            return 0
        elif black and player_color == 'black':
            return 1
        elif white and player_color == 'white':
            return 1
        else:
            return 2

    def _player_turn(self, player):
        """
        Perform a player's turn
        """
        if self._show_available:
            self._game.show_available_tiles(player.get_color())
            self.display_board()
            self._game.restore_tiles()

        print(f"{player.get_name()}'s turn")
        move = self._get_player_move(player.get_color())
        self._game.make_move(player.get_color(), move)
        self.display_board()

    def _first_turn(self):
        """
        Process inputs and outputs for the first turn, identifying the player color and symbol.
        """
        if self._show_available:
            self._game.show_available_tiles('black')
            self.display_board()
            self._game.restore_tiles()
        else:
            self.display_board()

        print(f"{self._player_1.get_name()}, you will go first! Your piece color is {self._player_1.get_color()}, "
              f"represented by the character 'X'")
        move_control = 0
        while move_control == 0:
            try:
                self._game.play_game(self._player_1.get_color(), self._get_player_move(self._player_1.get_color()))
            except InvalidMoveException:
                move_control -= 1
            move_control += 1

        if self._show_available:
            self._game.show_available_tiles('white')
            self.display_board()
            self._game.restore_tiles()
        else:
            self.display_board()

        print(f"{self._player_2.get_name()}, it is your turn! Your piece color is {self._player_2.get_color()}, "
              f"represented by the character 'O'")
        move_control = 0
        while move_control == 0:
            try:
                if self._player_2.get_name() == "PC":
                    self._computer_turn(self._player_2)
                else:
                    self._game.play_game(self._player_2.get_color(), self._get_player_move(self._player_2.get_color()))
            except InvalidMoveException:
                move_control -= 1
            move_control += 1

    def _computer_turn(self, player):
        """
        Perform the computer's turn
        """
        print(f"{player.get_name()}'s turn")
        if self._difficulty == 'random':
            move = random.choice(self._game.return_available_positions(player.get_color()))
        else:
            max_play = minimax(self._game.get_board(), 5, True)
            move = max_play[1]

        self._game.play_game(player.get_color(), move)
        self.display_board()

    def play_othello(self):
        """
        Play the Othello game, tracking rounds and checking if the game is over. Calls
        all other methods as necessary
        """
        self.create_players()
        self.available_tiles()

        if self._player_2.get_name() == "PC":
            self.choose_computer_difficulty()

        self._first_turn()

        round_tracker = 2
        should_continue = True
        while should_continue:
            game_status = self.game_status(self._player_1.get_color())
            if game_status == 0:
                print(f"\nGame Over!")
                self._game.print_scores(self._player_1, self._player_2)
                print(self._game.return_winner())
                return
            elif game_status == 2:
                self._player_turn(self._player_1)

            game_status = self.game_status(self._player_2.get_color())
            if game_status == 0:
                print(f"\nGame Over!")
                self._game.print_scores(self._player_1, self._player_2)
                print(self._game.return_winner())
                return
            elif game_status == 2:
                if self._player_2.get_name() == "PC":
                    self._computer_turn(self._player_2)
                else:
                    self._player_turn(self._player_2)

            print(f"Round {round_tracker} Complete")
            round_tracker += 1
            self._game.print_scores(self._player_1, self._player_2)

if __name__ == "__main__":
    game = NewGame()
    game.play_othello()
