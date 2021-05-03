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
