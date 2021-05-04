#!/usr/bin/env python3

import sys
from board import AgentBoard
from agent import *
import random


def walk(difficulty, seed):
    random.seed(seed)

    game = AgentBoard(difficulty) #
    agent = Agent()
    agent.newGame(game, True)
    agent.loadStateMemory()

    stop = ""
    gameOutput = CONTINUE_TEXT
    input(HELP_MESSAGE)
    while stop != "e" and gameOutput == CONTINUE_TEXT:
        gameOutput = agent.takeAction(True)
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
            elif(stop == "h" or stop == "help"):
                stop = input(HELP_MESSAGE)
            elif(stop == "e"):
                break
            else:
                stop = ""
    game.printGameState()
    input(gameOutput)

def simulateGame(agent, difficulty, iteration, wins):
    game = AgentBoard(difficulty) #
    train = True
    agent.newGame(game, train)

    gameOutput = CONTINUE_TEXT
    while gameOutput == CONTINUE_TEXT:
        gameOutput = agent.takeAction()

    if gameOutput == WIN_TEXT:
        wins += 1
    if(iteration % 1000 == 0):
        agent.storeStateMemory()
    if(iteration % 100 == 0):
        print("iteration: {:>5} win_percent: {:0.5f}".format(iteration, wins / (iteration + 1)))
    return wins

def train(difficulty, iterations, load = False):
    random.seed(random.randint(0, 1000000))
    iteration = 0
    wins = 0
    agent = Agent()
    if(load):
        agent.loadStateMemory()
    while(iteration < iterations):
        wins = simulateGame(agent, difficulty, iteration, wins)
        iteration += 1
    agent.storeStateMemory()
    print("iteration: {:>5} win_percent: {:0.5f}".format(iteration, wins / (iteration + 1)))


def main():
    difficulty = EASY_DIFFICULTY
    print("Minesweeper Solver...")
    while True:
        diff = "Easy"
        playerInput = input("""Options:
    train        (train the model)
    walk         (walk through the model's decisions)
    difficulty   (currently set to {})
    exit

    ... """.format(diff))
        playerInput = playerInput.strip() #remove trailiing white space
        playerInput.lower()

        if(playerInput == "train"):
            while playerInput.isnumeric() == False:
                playerInput = input("Number of Iterations: ")
                playerInput = playerInput.strip() #remove trailing white space
            iterations = int(playerInput)

            while playerInput != "y" and playerInput != "n":
                playerInput = input("Overwrite state memory? (y or n) ")
                playerInput = playerInput.lower().strip() #remove trailing white space

            load = False if playerInput == "y" else True
            train(difficulty, iterations, load)
        elif(playerInput == "walk"):
            while playerInput != "y" and playerInput != "n":
                playerInput = input("Set the random seed? (y or n) ")
                playerInput = playerInput.lower().strip() #remove trailing white space
            seed = random.randint(0, 1000000)
            if(playerInput == "y"):
                while playerInput.isnumeric() == False:
                    playerInput = input("Set Random Seed: ")
                seed = playerInput
            walk(difficulty, seed)
        elif(playerInput == "difficulty"):
            accepted = ["easy", "medium", "hard", "exit"]
            while playerInput not in accepted:
                playerInput = input("""Current Difficulty: {}
Options:
    easy      (10 mines, 10x10 board)
    medium    (10 mines, 10x10 board)
    hard      (10 mines, 10x10 board)
    exit

    ... """.format(diff))
                playerInput.lower().strip()
            if(playerInput == "easy"):
                difficulty = EASY_DIFFICULTY
            elif(playerInput == "medium"):
                difficulty = MEDIUM_DIFFICULTY
            elif(playerInput == "hard"):
                difficulty = HARD_DIFFICULTY

        elif(playerInput == "exit"):
            break
        else:
            continue


main()
