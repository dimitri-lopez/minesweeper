#!/usr/bin/env python3

MINE = 9

OUT_OF_BOUNDS = "x" #out of bounds

COVERED = 0
UNCOVERED = 1
FLAG = 2
CHECKED = 10

GAMEOVER_TEXT = "Game over!"
WIN_TEXT = "You won!"
CONTINUE_TEXT = "continue"


REWARD_PROGRESS = 0.3 # TODO add a multiplier so that the most squares are undone in a single click?
REWARD_GUESS = -0.3
REWARD_NO_CHANGE = -0.6
REWARD_GAMEOVER = -1

EASY_DIFFICULTY =   [10, 10, 10]
MEDIUM_DIFFICULTY = [18, 16, 40]
HARD_DIFFICULTY =   [30, 16, 99]

HELP_MESSAGE = """Walking Mode:
    h (print this screen)
    help (print this screen)
    a (list out actions)
    s (list out squares that need to be searched)
    m (list out the memory of all states (laggy))
    e (exit)

return to continue...
"""

surrounding = [
    [-1, -1],
    [-1,  0],
    [-1, 1],
    [0, -1],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1],
]
