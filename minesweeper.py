#!/usr/bin/env python
# pip install termcolor
# sudo pip3 install tk
# sudo pacman -S tk
import sys
from board import Board
from graphics import *

win = GraphWin()


game = Board(10, 10, 15)
play = True
while play:
    game.print()
    # game.printGameState()

    playerInput = ""
    repeat = True
    while repeat:
        playerInput = input("Your turn ( , f, c) (x, y):")
        playerInput = playerInput.strip()
        playerInput = playerInput.split(" ")
        if(len(playerInput) > 1):
            repeat = False

    output = game.parsePlayerInput(playerInput)


    # Reset the game
    if(output == "Game Over"):
        play = False
        playerInput = input("Play again? (y or n): ")
        if(playerInput.lower() == "y"):
            game = Board(10, 10, 15)
        else:
            play = False


# win = GraphWin()
# pt = Point(100, 50)
# pt.draw(win)
# cir = Circle(pt, 25)
# cir.draw(win)
