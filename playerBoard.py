#!/usr/bin/env python3
import random
from termcolor import colored
from enums import *

class Board:
    board = []   #game state board
    visible = [] #player visible board
    firstMove = True


    def __init__(self, rows, cols, mines, board = ""):
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.board = [[0 for i in range(cols)] for j in range(rows)]
        self.visible = [[0 for i in range(cols)] for j in range(rows)]

        self.placeMines(mines)

        if(board != ""): # random board
            self.importBoard(board)

    def importBoard(self, board):
        self.board = [
            [0,9,0,9,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]

    def printGameState(self):
        for y in range(self.cols):
            if(self.cols < 10):
                print("" + str((self.cols - y)) + " |", end = "")
            else:
                print("" + str((self.cols - y)//10) + str((self.cols - y)%10) + " |", end = "")

            for x in range(self.rows):
                self.printNumber(self.board[y][x])
                # if self.board[y][x] == MINE:
                #     print(" *", end = "")
                # elif self.board[y][x] == 0:
                #     print("  ", end = "")
                # else:
                #     print(" " + str(self.board[y][x]), end = "")

            print("")

        # Border
        if(self.cols < 10):
            print("  +", end = "")
        else:
            print("   +", end = "")
        for x in range(self.rows):
            print("--", end = "")
        print("-+")

        # One's digit
        if(self.cols < 10):
            print("  ", end = "")
        else:
            print("    ", end = "")
        for x in range(self.rows):
            print(" " + str((x+1) % 10), end = "")

        print()
        # tens digit
        if(self.cols > 9):
            print("    ", end = "")
        for x in range(self.rows):
            print(" " + str((x+1)// 10), end = "")

        print()

    def print(self):
        for y in range(self.cols):
            if(self.cols < 10):
                print("" + str((self.cols - y)) + " |", end = "")
            else:
                print("" + str((self.cols - y)//10) + str((self.cols - y)%10) + " |", end = "")

            for x in range(self.rows):
                if self.visible[y][x] == COVERED: #UNCOVERED
                    print(" .", end = "")
                elif self.visible[y][x] == FLAG:    #FLAG
                    print(" F", end = "")
                else:                               #Number
                    self.printNumber(self.board[y][x])

            print("")

        # Border
        if(self.cols < 10):
            print("  +", end = "")
        else:
            print("   +", end = "")
        for x in range(self.rows):
            print("--", end = "")

        print("-+")

        # One's digit
        if(self.cols < 10):
            print("  ", end = "")
        else:
            print("    ", end = "")
        for x in range(self.rows):
            print(" " + str((x+1) % 10), end = "")

        print()
        # tens digit
        if(self.cols > 9):
            print("    ", end = "")
        for x in range(self.rows):
            print(" " + str((x+1)// 10), end = "")

        print()

    def printNumber(self, num):
        colors = [
            "",
            "blue",     #1
            "green",    #2
            "red",      #3
            "yellow",   #4
            "grey",     #5
            "magenta",  #6
            "cyan",     #7
            "white"]    #8
        print(" ", end = "")
        if num == MINE:
            print(colored("*", "white", attrs= ["dark", "bold", "blink"]), end = "")
        elif num == 0:
            print(" ", end = "")
        else:
            print(colored(str(num), colors[num]), end = "")


    def placeMines(self, mines):
        currentMines = 0
        while currentMines < mines:
            if self.placeMine():
                currentMines += 1;

    def placeMine(self):
        x = random.randrange(0, self.rows)
        y = random.randrange(0, self.rows)
        if(self.board[y][x] == 9):
            return False
        else:
            self.board[y][x] = MINE
            return True


    def inBoard(self, y, x):
        return y >= 0 and y < self.rows and x >= 0 and x < self.cols

    def notInBoard(self, y, x):
        return not(self.inBoard(y,x))

    def removeSurroundingMines(self, y, x):
        movedMines = 0

        if(self.board[y][x] == MINE):
            self.board[y][x] = 0
            movedMines += 1
            # print("Found a mine at " + str(x) + ", " + str(y))


        for i in surrounding:
            dy = y + i[0]
            dx = x + i[1]

            if(self.notInBoard(dy, dx)):
                continue

            if(self.board[dy][dx] == MINE):
                # self.printGameState()
                # input("Found a mine at " + str(dy) + ", " + str(dx))
                self.board[dy][dx] = 0
                movedMines += 1
        return movedMines

    def updateNumbers(self):
        for y in range(self.cols):
            for x in range(self.rows):
                if(self.board[y][x] == MINE):
                    continue
                count = 0

                for i in surrounding:
                    dy = y + i[0]
                    dx = x + i[1]

                    if(self.inBoard(dy, dx)):
                            if(self.board[dy][dx] == MINE):
                                count += 1
                self.board[y][x] = count

    def firstMove(self, y, x):
        movedMines = 1;
        while(movedMines != 0):
            movedMines = self.removeSurroundingMines(y, x)
            self.placeMines(movedMines)

        self.updateNumbers()


    def uncover(self, y, x):
        if(self.visible[y][x] == UNCOVERED): #Already visited by the algorithm
            return

        self.visible[y][x] = UNCOVERED  #Uncover the square

        if(self.board[y][x] != 0): #Numbered squares don't need to uncover more
            return
        for i in surrounding: #Uncover surrounding squares if zero
            dy = y + i[0]
            dx = x + i[1]
            if(self.inBoard(dy, dx)):
                self.uncover(dy, dx)

    def parsePlayerInput(self, playerInput):
        if(len(playerInput) == 3):
            y = int(playerInput[2])
            x = int(playerInput[1])
        else:
            y = int(playerInput[1])
            x = int(playerInput[0])

        y = self.cols - y
        x = x - 1

        if(self.notInBoard(y, x)):
            return "invalid"

        if(playerInput[0] == 'f'):   # Flag
            return self.flag(y, x)
        elif(playerInput[0] == 'c'): # Chord
            return self.chord(y, x)
        else:                        # Move
            return self.move(y, x)


    def move(self, y, x):
        if(self.firstMove): #first move?
            self.firstMove(y, x)
            self.firstMove = False
        elif(self.board[y][x] == MINE):
            self.printGameState()
            # print("Game Over")
            return "Game Over"
        elif(self.visible[y][x] == FLAG or self.visible[y][x] == UNCOVERED):
            return "next"


        self.uncover(y, x)
        return "next"

    def flag(self, y, x):
        if(self.visible[y][x] == COVERED):
            self.visible[y][x] = FLAG
        else:
            return "next"

    def chord(self, y, x):
        flagCount = 0
        for i in surrounding:
            dy = y + i[0]
            dx = x + i[1]
            if(self.notInBoard(dy, dx)):
                continue
            if(self.visible[dy][dx] == FLAG):
                flagCount += 1

        if(self.board[y][x] == flagCount): #Correct number of flags found
            for i in surrounding:
                dy = y + i[0]
                dx = x + i[1]
                output = self.move(dy, dx)
                if(output == "Game Over"):
                    return "Game Over"

