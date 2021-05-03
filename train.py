#!/usr/bin/env python3

import sys
from board import AgentBoard
from agent import *
import random


MAX_ITERATIONS = 10000
# random.seed(1)


def simulateGame(agent, iteration, wins):
    game = AgentBoard(10, 10, 10, iteration) #
    train = True
    agent.newGame(game, train)

    gameOutput = CONTINUE_TEXT
    while gameOutput == CONTINUE_TEXT:
        gameOutput = agent.takeAction()

    if gameOutput == WIN_TEXT:
        wins += 1
    if(iteration % 1000 == 0):
        agent.storeStateMemory()
    if(iteration % 250 == 0):
        print("iteration: {:>5} win_percent: {:0.5f}".format(iteration, wins / (iteration + 1)))
    return wins

def main():
    iteration = 0
    wins = 0
    agent = Agent()
    agent.loadStateMemory()
    while(iteration < MAX_ITERATIONS):
        wins = simulateGame(agent, iteration, wins)
        iteration += 1
    print("iteration: {:>5} win_percent: {:0.5f}".format(iteration, wins / (iteration + 1)))
main()
