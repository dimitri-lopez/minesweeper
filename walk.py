#!/usr/bin/env python3

import sys
import random
from board import AgentBoard
from agent import *

# random.seed(3)

game = AgentBoard(10, 10, 10, 0) #
agent = Agent()
agent.newGame(game, True)
agent.loadStateMemory()
agent.printStateMemory()

stop = ""
gameOutput = CONTINUE_TEXT
while stop != "e" and gameOutput == CONTINUE_TEXT:
    gameOutput = agent.takeAction()
    game.print()

    stop = input("...")
    while stop != "":
        if(stop == "m"):
            agent.printStateMemory()
            stop = input("...")
        elif(stop == "a"):
            agent.printActions()
            stop = input("...")
        elif(stop == "s"):
            agent.printSearch()
            stop = input("...")
        else:
            stop = ""
print(gameOutput)
