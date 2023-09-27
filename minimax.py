# Author: Austin Cooper
# GitHub username: amcooper181
# Uses several class methods from the Othello class for standalone board simulation.


import copy
from othello_class import DIRECTIONS


def create_next_index(current_index, direct):
    """
    Adapted from Othello class methods for the minimax function, does not make any changes to the game object.
    """
    row, col = current_index
    delta_row, delta_col = DIRECTIONS[direct]
    new_row, new_col = row + delta_row, col + delta_col
    return new_row, new_col


def capture_tiles(board, piece, opp_piece, current_index, direct, first_move=0, tiles_captured=None):
    """
    Adapted from Othello class methods for the minimax function, does not make any changes to the game object.
    """
    new_index = create_next_index(current_index, direct)
    row, column = new_index
    if first_move == 0:
        tiles_captured = []
    tiles_captured.append(new_index)
    if board[row][column] == '*':
        return
    if board[row][column] == '.':
        return
    if board[row][column] == piece and first_move == 0:
        return
    if board[row][column] == piece:
        return True
    if board[row][column] == opp_piece:
        first_move += 1
        if capture_tiles(board, piece, opp_piece, new_index, direct, first_move, tiles_captured) is True:
            for tile in tiles_captured:
                x, y = tile
                board[x][y] = piece


def make_move(board, color, piece_position):
    """
    Adapted from Othello class methods for the minimax function, does not make any changes to the game object.
    """
    if color == 'black':
        piece = 'X'
        opp_piece = 'O'
    elif color == 'white':
        piece = 'O'
        opp_piece = 'X'

    row, col = piece_position
    board[row][col] = piece

    for direction in DIRECTIONS:
        capture_tiles(board, piece, opp_piece, piece_position, direction)


def return_available_positions(board, color):
    """
    Adapted from Othello class methods for the minimax function, does not make any changes to the game object.
    """
    available_positions = []
    if color == 'black':
        piece = "X"
        opp_piece = "O"
    elif color == 'white':
        piece = "O"
        opp_piece = "X"
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == piece:
                current_index = (x,y)
                valid_moves = check_valid_moves(board, piece, opp_piece, current_index)
                for item in valid_moves:
                    if item is not None:
                        if item not in available_positions:
                            available_positions.append(item)
    available_positions.sort()
    return available_positions


def check_valid_moves(board, piece, opp_piece, current_index):
    """
    Adapted from Othello class methods for the minimax function, does not make any changes to the game object.
    """
    up = check_direction(board, piece, opp_piece, current_index, 'u')
    down = check_direction(board, piece, opp_piece, current_index, 'd')
    left = check_direction(board, piece, opp_piece, current_index, 'l')
    right = check_direction(board, piece, opp_piece, current_index, 'r')
    up_left = check_direction(board, piece, opp_piece, current_index, 'ul')
    up_right = check_direction(board, piece, opp_piece, current_index, 'ur')
    down_left = check_direction(board, piece, opp_piece, current_index, 'dl')
    down_right = check_direction(board, piece, opp_piece, current_index, 'dr')
    valid_moves = [up, down, left, right, up_left, up_right, down_left, down_right]
    return valid_moves


def check_direction(board, piece, opp_piece, current_index, direct, first_move=0):
    """
    Adapted from Othello class methods for the minimax function, does not make any changes to the game object.
    """
    new_index = create_next_index(current_index, direct)
    row, column = new_index
    if board[row][column] == "*":
        return
    elif board[row][column] == "." and first_move == 0:
        return
    elif board[row][column] == "." and first_move > 0:
        return row, column
    elif board[row][column] == opp_piece:
        first_move += 1
        return check_direction(board, piece, opp_piece, new_index, direct, first_move)


def game_over(board):
    """
    Adapted from Othello class methods for the minimax function, does not make any changes to the game object.
    """
    avail_moves_white = return_available_positions(board, 'white')
    avail_moves_black = return_available_positions(board, 'black')

    if avail_moves_white == 0 and avail_moves_black == 0:
        return True


def get_score(board):
    """
    Adapted from Othello class methods for the minimax function, does not make any changes to the game object.
    """
    black_score = sum(row.count('X') for row in board)
    white_score = sum(row.count('O') for row in board)
    return white_score - black_score


def minimax(current_board, depth, maximizing_player):
    """
    Return an optimal move using a minimax algorithm given a depth and the current board.
    """
    if depth == 0 or game_over(current_board):
        return get_score(current_board), None

    if maximizing_player:
        max_evaluation = float('-inf'), None
        avail_moves = return_available_positions(current_board, 'white')
        for move in avail_moves:
            game_board_copy = copy.deepcopy(current_board)
            make_move(game_board_copy, 'white', move)
            val, _ = minimax(game_board_copy, depth - 1, False)

            if val > max_evaluation[0]:
                max_evaluation = val, move

        return max_evaluation

    else:
        min_evaluation = float('+inf'), None
        avail_moves = return_available_positions(current_board, 'black')
        for move in avail_moves:
            game_board_copy = copy.deepcopy(current_board)
            make_move(game_board_copy, 'black', move)
            val, _ = minimax(game_board_copy, depth - 1, True)

            if val < min_evaluation[0]:
                min_evaluation = val, move

        return min_evaluation

