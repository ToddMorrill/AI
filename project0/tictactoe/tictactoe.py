"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None
recursion_counter = 0


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counts = {EMPTY: 0, X: 0, O: 0}
    for row in board:
        for val in row:
            counts[val] += 1
    # initially X goes first (per specification)
    if counts[EMPTY] == 9:
        return X
    elif counts[X] > counts[O]:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == EMPTY:
                action_set.add((i, j))
    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    action_set = actions(board)
    if action not in action_set:
        raise ValueError(f'{action} not in action set.')

    # whose turn is it?
    current_player = player(board)

    # per hint
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    X_win = [X, X, X]
    O_win = [O, O, O]
    # check rows
    for row in board:
        if row == X_win:
            return X
        elif row == O_win:
            return O

    # check cols
    for col in range(len(board[0])):
        complete_column = []
        for row in range(len(board)):
            complete_column.append(board[row][col])
        if complete_column == X_win:
            return X
        elif complete_column == O_win:
            return O

    # check diagonals
    diagonal_one = [board[i][i] for i in range(len(board))]
    diagonal_two = [board[i][len(board) - 1 - i] for i in range(len(board))]
    for diagonal in [diagonal_one, diagonal_two]:
        if diagonal == X_win:
            return X
        elif diagonal == O_win:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check if there's a winner
    if winner(board) is not None:
        return True

    # check if the board is full
    if len(actions(board)) == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_result = winner(board)
    if game_result == X:
        return 1
    elif game_result == O:
        return -1
    else:
        return 0


def min_value(board):
    #recording metrics
    global recursion_counter
    recursion_counter += 1

    if terminal(board):
        return utility(board)
    value = float('inf')
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value


def max_value(board):
    # recording metrics
    global recursion_counter
    recursion_counter += 1

    if terminal(board):
        return utility(board)
    value = -float('inf')
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # whose turn is it?
    current_player = player(board)

    # recording metrics
    global recursion_counter
    if current_player == X:
        max_action = None
        max_utility = -float('inf')
        for action in actions(board):
            action_utility = min_value(result(board, action))
            if action_utility > max_utility:
                max_action = action
                max_utility = action_utility
        # recording metrics
        print(recursion_counter)
        recursion_counter = 0
        return max_action
    else:
        min_action = None
        min_utility = float('inf')
        for action in actions(board):
            action_utility = max_value(result(board, action))
            if action_utility < min_utility:
                min_action = action
                min_utility = action_utility
        # recording metrics
        print(recursion_counter)
        recursion_counter = 0
        return min_action

if __name__ == '__main__':
    minimax(initial_state())