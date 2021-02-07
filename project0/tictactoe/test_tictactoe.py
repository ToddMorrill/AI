import time

import pytest

from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax
from tictactoe import X, O, EMPTY


@pytest.fixture()
def O_goes():
    return [[X, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


@pytest.fixture()
def X_goes():
    return [[X, O, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


@pytest.fixture()
def X_went():
    return [[X, O, X], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


@pytest.fixture()
def X_winner_row():
    return [[X, X, X], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


@pytest.fixture()
def X_winner_col():
    return [[X, EMPTY, EMPTY], [X, EMPTY, EMPTY], [X, EMPTY, EMPTY]]


@pytest.fixture()
def X_winner_diagonal_one():
    return [[X, EMPTY, EMPTY], [EMPTY, X, EMPTY], [EMPTY, EMPTY, X]]


@pytest.fixture()
def X_winner_diagonal_two():
    return [[EMPTY, EMPTY, X], [EMPTY, X, EMPTY], [X, EMPTY, EMPTY]]


@pytest.fixture()
def O_winner_row():
    return [[O, O, O], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


@pytest.fixture()
def O_winner_col():
    return [[O, EMPTY, EMPTY], [O, EMPTY, EMPTY], [O, EMPTY, EMPTY]]


@pytest.fixture()
def O_winner_diagonal_one():
    return [[O, EMPTY, EMPTY], [EMPTY, O, EMPTY], [EMPTY, EMPTY, O]]


@pytest.fixture()
def O_winner_diagonal_two():
    return [[EMPTY, EMPTY, O], [EMPTY, O, EMPTY], [O, EMPTY, EMPTY]]


@pytest.fixture()
def full_board_no_winner():
    return [[X, O, X], [X, O, O], [O, X, X]]


def test_player_initial_state():
    board = initial_state()
    assert player(board) == 'X'


def test_player_O_goes(O_goes):
    board = O_goes
    assert player(board) == 'O'


def test_player_X_goes(X_goes):
    board = X_goes
    assert player(board) == 'X'


def test_actions_complete():
    board = initial_state()
    assert len(actions(board)) == 9


def test_actions_odd(O_goes):
    board = O_goes
    action_set = actions(board)
    assert len(action_set) == 8
    assert (0, 0) not in action_set


def test_actions_even(X_goes):
    board = X_goes
    action_set = actions(board)
    assert len(action_set) == 7
    assert ((0, 0) not in action_set) and ((0, 1) not in action_set)


def test_result_valueerror(O_goes):
    board = O_goes
    with pytest.raises(ValueError, match=r'\(0, 0\) not in action set.'):
        result(board, (0, 0))


def test_result_X_moves(X_goes, X_went):
    board = X_goes
    assert result(board, (0, 2)) == X_went


def test_winner_X_row(X_winner_row):
    board = X_winner_row
    assert winner(board) == X


def test_winner_X_col(X_winner_col):
    board = X_winner_col
    assert winner(board) == X


def test_winner_X_diagonal_one(X_winner_diagonal_one):
    board = X_winner_diagonal_one
    assert winner(board) == X


def test_winner_X_diagonal_two(X_winner_diagonal_two):
    board = X_winner_diagonal_two
    assert winner(board) == X


def test_winner_O_row(O_winner_row):
    board = O_winner_row
    assert winner(board) == O


def test_winner_O_col(O_winner_col):
    board = O_winner_col
    assert winner(board) == O


def test_winner_O_diagonal_one(O_winner_diagonal_one):
    board = O_winner_diagonal_one
    assert winner(board) == O


def test_winner_O_diagonal_two(O_winner_diagonal_two):
    board = O_winner_diagonal_two
    assert winner(board) == O


def test_terminal_winner(X_winner_row):
    board = X_winner_row
    assert terminal(board)


def test_terminal_no_winner(full_board_no_winner):
    board = full_board_no_winner
    assert terminal(board)


def test_terminal_in_progress(O_goes):
    board = O_goes
    assert not terminal(board)


def test_utility_X_winner(X_winner_row):
    board = X_winner_row
    assert utility(board) == 1


def test_utility_O_winner(O_winner_row):
    board = O_winner_row
    assert utility(board) == -1


def test_utility_no_winner(full_board_no_winner):
    board = full_board_no_winner
    assert utility(board) == 0


def test_minimax_empty_board(capsys):
    global recursion_counter
    recursion_counter = 0
    board = initial_state()
    start = time.time()
    action = minimax(board)
    end = time.time()
    duration = end - start
    assert duration > 29
    out, err = capsys.readouterr()
    assert out == '549945\n'