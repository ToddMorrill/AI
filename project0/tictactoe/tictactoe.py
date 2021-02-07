"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None
recursion_counter = 0


def initial_state() -> list:
    """Returns starting state of the board.

    Returns:
        list: List of lists containing initial game board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: list) -> str:
    """Returns player who has the next turn on a board.

    Args:
        board (list): List of lists containing the current game board.

    Returns:
        str: Current player.
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


def actions(board: list) -> set:
    """Returns set of all possible actions (i, j) available on the board.

    Args:
        board (list): List of lists containing the current game board.

    Returns:
        set: Set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == EMPTY:
                action_set.add((i, j))
    return action_set


def result(board: list, action: tuple) -> list:
    """Returns the board that results from making move (i, j) on the board.

    Args:
        board (list): List of lists containing the current game board.
        action (tuple): Position (i, j) where the current player moves.

    Raises:
        ValueError: If action not in action set.

    Returns:
        list: List of lists containing the new game board.
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


def winner(board: list) -> str:
    """Returns the winner of the game, if there is one.

    Args:
        board (list): List of lists containing the current game board.

    Returns:
        str: Player who won, if any.
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


def terminal(board: list) -> bool:
    """Returns True if game is over, False otherwise.

    Args:
        board (list): List of lists containing the current game board.

    Returns:
        bool: True if game is over, otherwise False.
    """
    # check if there's a winner
    if winner(board) is not None:
        return True

    # check if the board is full
    if len(actions(board)) == 0:
        return True

    return False


def utility(board: list) -> int:
    """Returns 1 if X has won the game, -1 if O has won, 0 otherwise.

    NB: this function should only be called in if terminal(board) == True.

    Args:
        board (list): List of lists containing the current game board.

    Returns:
        int: Value of the game board.
    """
    game_result = winner(board)
    if game_result == X:
        return 1
    elif game_result == O:
        return -1
    else:
        return 0


def min_value(board: list, alpha: int, beta: int) -> int:
    """Min player's function to determine the value of the current board state.

    Args:
        board (list): List of lists containing the current game board.
        alpha (int): The value of the best choice found so far for the max 
        player.
        beta (int): The value of the best choice found so far for the min 
        player.

    Returns:
        int: Value of the current board state.
    """
    #recording metrics
    global recursion_counter
    recursion_counter += 1

    if terminal(board):
        return utility(board)
    value = float('inf')
    for action in actions(board):
        value = min(value, max_value(result(board, action), alpha, beta))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def max_value(board: list, alpha: int, beta: int) -> int:
    """Max player's function to determine the value of the current board state.

    Args:
        board (list): List of lists containing the current game board.
        alpha (int): The value of the best choice found so far for the max 
        player.
        beta (int): The value of the best choice found so far for the min 
        player.

    Returns:
        int: Value of the current board state.
    """
    # recording metrics
    global recursion_counter
    recursion_counter += 1

    if terminal(board):
        return utility(board)
    value = -float('inf')
    for action in actions(board):
        value = max(value, min_value(result(board, action), alpha, beta))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def minimax(board: int) -> tuple:
    """Returns the optimal action for the current player on the board. This
    function uses Alpha-Beta pruning to reduce computation.

    Args:
        board (int): List of lists containing the current game board.

    Returns:
        tuple: Best action (i, j) for the current player.
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
            action_utility = min_value(result(board, action), -float('inf'),
                                       float('inf'))
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
            action_utility = max_value(result(board, action), -float('inf'),
                                       float('inf'))
            if action_utility < min_utility:
                min_action = action
                min_utility = action_utility
        # recording metrics
        print(recursion_counter)
        recursion_counter = 0
        return min_action


if __name__ == '__main__':
    minimax(initial_state())