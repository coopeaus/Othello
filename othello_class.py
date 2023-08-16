# Author: Austin Cooper
# GitHub username: amcooper181

import copy

DIRECTIONS = {
    'u': (-1, 0),
    'd': (1, 0),
    'l': (0, -1),
    'r': (0, 1),
    'ul': (-1, -1),
    'ur': (-1, 1),
    'dl': (1, -1),
    'dr': (1, 1)
}


class InvalidMoveException(Exception):
    pass


class Player:
    """
    Represent a player for the board game Othello, with a given name and color. 'black' = X piece, and 'white'
    = O piece.
    """
    def __init__(self, player_name, piece_color):
        self._player_name = player_name
        self._color = piece_color

    def get_name(self):
        """Return the player name"""
        return self._player_name

    def get_color(self):
        """Return the player color"""
        return self._color

    def set_name(self, name):
        """Re-set the player name"""
        self._player_name = name

    def set_color(self, color):
        """Re-set the player color"""
        self._color = color


class Othello:
    """
    Represent the game Othello. The object contains the game board, a list of players, their scores, and a list
    of available positions. The board will be initialized to its default state, the player scores will be initialized
    to two each (default at the beginning of game) and the lists will be initialized as empty lists. The create_player
    method will create a Player object.
    """
    def __init__(self):
        self._board = [
            ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", "O", "X", ".", ".", ".", "*"],
            ["*", ".", ".", ".", "X", "O", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],
            ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"]
        ]
        self._saved_board = []
        self._player_list = []
        self._available_positions = []
        self._black_score = 2
        self._white_score = 2
        self._saved_scores = 2, 2

    def get_scores(self):
        """Return a tuple containing the current scores"""
        return self._black_score, self._white_score

    def print_scores(self, player_1, player_2):
        """Print the current scores"""
        print(f"Scores: \n"
              f"{player_1.get_name()}: {self._black_score} \n"
              f"{player_2.get_name()}: {self._white_score} \n")

    def print_board(self):
        """Print the current state of the Othello board"""
        for row in self._board:
            print(*(' '.join(row)))

    def save_state(self):
        """Save the current state of the Othello game, used when the computer analyzes available moves"""
        self._saved_board = copy.deepcopy(self._board)
        self._saved_scores = self._black_score, self._white_score

    def restore_state(self):
        """Restore the Othello game to the most recent saved state, used when the computer analyzes available moves"""
        self._board = copy.deepcopy(self._saved_board)
        self._black_score, self._white_score = self._saved_scores

    def add_player(self, player_object):
        """Create a player object with a given name and piece color"""
        self._player_list.append(player_object)

    def check_valid_moves(self, piece, opp_piece, current_index):
        """Check to see if there is a valid move in any direction given a piece, opponents piece, and current index.
            Return the list of valid moves. Helper method for the check_direction method."""
        up = self.check_direction(piece, opp_piece, current_index, 'u')
        down = self.check_direction(piece, opp_piece, current_index, 'd')
        left = self.check_direction(piece, opp_piece, current_index, 'l')
        right = self.check_direction(piece, opp_piece, current_index, 'r')
        up_left = self.check_direction(piece, opp_piece, current_index, 'ul')
        up_right = self.check_direction(piece, opp_piece, current_index, 'ur')
        down_left = self.check_direction(piece, opp_piece, current_index, 'dl')
        down_right = self.check_direction(piece, opp_piece, current_index, 'dr')
        valid_moves = [up, down, left, right, up_left, up_right, down_left, down_right]
        return valid_moves

    def create_next_index(self, current_index, direct):
        """Returns the next index when traveling in a given direction, given a current index. Used in the
           check_direction and capture_tiles methods."""
        row, col = current_index
        delta_row, delta_col = DIRECTIONS[direct]
        new_row, new_col = row + delta_row, col + delta_col
        return new_row, new_col

    def check_direction(self, piece, opp_piece, current_index, direct, first_move=0):
        """
        Given a piece, opponent piece, the current index, and a direction to check in, checks for a valid move.
        Returns the row and column of index if the direction results in a move that is valid. Uses the
        create_next_index method to find the next index in the given direction. First_move has a default value of 0,
        and is incremented when an opponent piece is found, to only return a move for an empty space if there was
        already an opponent's piece found in that direction.
        """
        new_index = self.create_next_index(current_index, direct)
        row, column = new_index
        if self._board[row][column] == "*":
            return
        elif self._board[row][column] == "." and first_move == 0:
            return
        elif self._board[row][column] == "." and first_move > 0:
            return row, column
        elif self._board[row][column] == opp_piece:
            first_move += 1
            return self.check_direction(piece, opp_piece, new_index, direct, first_move)

    def return_available_positions(self, color):
        """Return a list of positions that the player with the given color can play on the current board"""
        self._available_positions = []
        if color == 'black':
            piece = "X"
            opp_piece = "O"
        elif color == 'white':
            piece = "O"
            opp_piece = "X"
        for x in range(len(self._board)):
            for y in range(len(self._board[x])):
                if self._board[x][y] == piece:
                    current_index = (x,y)
                    valid_moves = self.check_valid_moves(piece, opp_piece, current_index)
                    for item in valid_moves:
                        if item is not None:
                            if item not in self._available_positions:
                                self._available_positions.append(item)
        self._available_positions.sort()
        return self._available_positions

    def capture_tiles(self, piece, opp_piece, current_index, direct, first_move=0, tiles_captured=None):
        """
        Given the index where a piece is placed, the color of that piece, the opponents piece, and a direction, check
        that direction for at least one opponent's piece immediately adjacent followed by the player's piece. Append
        each new index to the tiles_captured list. If a valid capture is found, flip all the tiles in the
        tiles_captured list. first_move has a default value of 0 for the case where a player's piece is found
        immediately adjacent. tiles_captured has a default value of None and is initialized to an empty list, with
        each tile visited appended to it.
        """
        new_index = self.create_next_index(current_index, direct)
        row, column = new_index
        if first_move == 0:
            tiles_captured = []
        tiles_captured.append(new_index)
        if self._board[row][column] == '*':
            return
        if self._board[row][column] == '.':
            return
        if self._board[row][column] == piece and first_move == 0:
            return
        if self._board[row][column] == piece:
            return True
        if self._board[row][column] == opp_piece:
            first_move += 1
            if self.capture_tiles(piece, opp_piece, new_index, direct, first_move, tiles_captured) is True:
                for tile in tiles_captured:
                    x, y = tile
                    self._board[x][y] = piece

    def make_move(self, color, piece_position):
        """
        Add a piece of a specified color to a specified board position (row, column), perform any color flips, and
        return the new board. Update the score, so that it is tracked after every move.
        """
        if color == 'black':
            piece = 'X'
            opp_piece = 'O'
        elif color == 'white':
            piece = 'O'
            opp_piece = 'X'

        row, col = piece_position
        self._board[row][col] = piece

        for direction in DIRECTIONS:
            self.capture_tiles(piece, opp_piece, piece_position, direction)

        self._black_score = sum(row.count('X') for row in self._board)
        self._white_score = sum(row.count('O') for row in self._board)

        return self._board

    def play_game(self, player_color, piece_position):
        """
        Given the player's color and selected piece position, attempt to add the piece to the position. If this is
        not a possible move, return an error, otherwise make the move. Check if either player has a move available, if
        so continue, if not the game is over and return the return_winner method.
        """
        possible_moves = self.return_available_positions(player_color)
        if piece_position not in possible_moves:
            print("Invalid move! Please try again.")
            print(f"Here are the valid moves: {possible_moves} \n")
            raise InvalidMoveException
        self.make_move(player_color, piece_position)

    def show_available_tiles(self, color):
        """Shows the available tiles for the player"""
        avail = self.return_available_positions(color)
        for coord in avail:
            row, column = coord
            self._board[row][column] = 'A'

    def restore_tiles(self):
        """Removes the 'A' from all available tiles so that the rest of the code will work"""
        for x in range(len(self._board)):
            for y in range(len(self._board[x])):
                if self._board[x][y] == 'A':
                    self._board[x][y] = '.'

    def return_winner(self):
        """Return the winner of the Othello game. The winner is the player with the most pieces on the board
           at game end."""
        if self._black_score == self._white_score:
            return "It's a tie"
        elif self._black_score > self._white_score:
            winning_color = 'black'
        else:
            winning_color = 'white'
        for player in self._player_list:
            if player.get_color() == winning_color:
                return f"Winner is: {player.get_name()}."


