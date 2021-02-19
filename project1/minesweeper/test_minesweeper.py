import pytest

from minesweeper import Minesweeper, MinesweeperAI

def check_mines(game, ai):
    mines = set()
    for i, row in enumerate(game.board):
        for j, col in enumerate(row):
            if col:
                mines.add((i, j))
    if mines != ai.mines:
        breakpoint()
    assert mines == ai.mines

def play_game():
    game = Minesweeper()
    ai = MinesweeperAI()

    # Keep track of revealed cells, flagged cells, and if a mine was hit
    revealed = set()
    flags = set()
    lost = False

    move = None

    while not lost:
        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                # won game
                check_mines(game, ai)
                break
        if move:
            if game.is_mine(move):
                lost = True
            else:
                nearby = game.nearby_mines(move)
                ai.add_knowledge(move, nearby)
    return lost

def test_win_rate():
    wins = 0
    games = 10000
    for _ in range(games):
        if not play_game():
            wins += 1
    win_rate = wins/games
    print(f'Won {wins}/{games} games.')
    assert (win_rate > .6)

if __name__ == '__main__':
    test_win_rate()
    