#!/usr/bin/env python
import random
from termcolor import colored
from enums import *
from agent import Agent


# random.seed(8)

class AgentBoard:
    board = []   #game state board
    visible = [] #player visible board
    firstMove = True
    reward = 0
    uncovered = 0
    flags = 0


    def __init__(self, rows, cols, mines, randomSeed = 0):
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.board = [[0 for i in range(cols)] for j in range(rows)]
        self.visible = [[0 for i in range(cols)] for j in range(rows)]

        self.placeMines(mines)

        # if(randomSeed != 0): # random board
            # random.seed(randomSeed)

    def printGameState(self):
        for y in range(self.cols):
            if(self.cols < 10):
                print("" + str(y) + " |", end = "")
            else:
                print("" + str((y)//10) + str((y)%10) + " |", end = "")

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
            print(" " + str((x) % 10), end = "")

        print()
        # tens digit
        if(self.cols > 9):
            print("    ", end = "")
        for x in range(self.rows):
            print(" " + str((x)// 10), end = "")

        print()

    def print(self):
        for y in range(self.cols):
            if(self.cols < 10):
                print("" + str(y) + " |", end = "")
            else:
                print("" + str(y//10) + str(y%10) + " |", end = "")

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
            print(" " + str((x) % 10), end = "")

        print()
        # tens digit
        if(self.cols > 9):
            print("    ", end = "")
        for x in range(self.rows):
            print(" " + str((x)// 10), end = "")

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


    def uncover(self, y, x, agent):
        if(self.visible[y][x] == UNCOVERED): #Already visited by the algorithm
            return

        self.visible[y][x] = UNCOVERED  #Uncover the square
        self.uncovered += 1


        # guess = True
        # for i in surrounding: # See if this is a guess or not
        #     dy = y + i[0]
        #     dx = x + i[1]
        #     if(self.inBoard(dy, dx)):
        #         if(self.visible[y][x] == UNCOVERED): #at least one square is uncovered, not a guess
        #             guess = False
        # # self.reward += REWARD_GUESS if guess else REWARD_PROGRESS # update based on if it was a guess

        if(self.board[y][x] != 0): #Numbered squares don't need to uncover more
            agent.addToSearch((y, x)) # TODO This might break stuff?
            return
        for i in surrounding: #Uncover surrounding squares if zero
            dy = y + i[0]
            dx = x + i[1]
            if(self.inBoard(dy, dx)):
                self.uncover(dy, dx, agent)

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


    def move(self, y, x, agent):
        if(self.firstMove): #first move?
            self.firstMove(y, x)
            self.firstMove = False
        elif(self.visible[y][x] == FLAG):
            return CONTINUE_TEXT
        elif(self.board[y][x] == MINE):
            # self.printGameState()
            # print("Game Over")
            # self.reward = REWARD_GAMEOVER
            # self.printGameState()
            return GAMEOVER_TEXT
        elif(self.visible[y][x] == FLAG or self.visible[y][x] == UNCOVERED):
            # self.reward += REWARD_NO_CHANGE
            return CONTINUE_TEXT

        self.uncover(y, x, agent)

        return self.checkWin()

    def checkWin(self):
        if(self.flags > self.mines):
            # self.printGameState()
            return GAMEOVER_TEXT
        elif(self.uncovered == (self.rows * self.cols - self.mines)):
            return WIN_TEXT
        else:
            return CONTINUE_TEXT

    def flag(self, y, x):
        if(self.visible[y][x] == COVERED):
            self.flags += 1
            self.visible[y][x] = FLAG
        return self.checkWin()

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

    def getState(self): # This will be what the agent can see
        typesOfActions = ["uncover"] #only uncover for now, we will add flag and chord later on
        state = "" #Just a string for now
        for y in range(self.cols):
            for x in range(self.rows):
                if self.visible[y][x] == COVERED: #UNCOVERED
                    state += "."
                    # visibleBoard[y][x] = "."
                elif self.visible[y][x] == FLAG:    #FLAG
                    # visibleBoard[y][x] = "F"
                    state += "F"
                else:                               #Number
                    state += str(board[y][x])
                    # visibleBoard[y][x] = board[y][x]
        return state
    def getCovered(self):
        for y in range(self.cols):
            for x in range(self.rows):
                if(self.visible[y][x] == COVERED):
                    return(y, x)

    # def getActions(self): # All possible actions that the agent can take
    #     actions = []
    #     for y in range(self.cols):
    #         for x in range(self.rows):
    #             actions.append(Action(y, x, "uncover"))
    #     return actions

    # def takeAction(self, action):
    #     # self.reward = 0
    #     if action.action == "uncover":
    #         move(action.y, action.x)

    #     return self.reward, self.getState() # add in the state?

    def isNumber(self, y, x):
        if(self.visible[y][x] == COVERED):
            return False
        if(self.board[y][x] != 0 and self.board[y][x] < MINE):
            return True
        else:
            return False
    def isFlag(self, y, x):
        return True if self.visible[y][x] == FLAG else False

    def isMine(self, y, x):
        return True if self.board[y][x] == MINE else False
    def isUncovered(self, y, x):
        return True if self.visible[y][x] == UNCOVERED else False


    def getSquare(self, y, x):
        if(self.notInBoard(y, x)):
            return "x"
        elif(self.isFlag(y, x)):
            return "F"
        elif(self.visible[y][x] == COVERED):
            # if(self.board[y][x] == MINE):
            #     return "*"
            return "."
        else:
            if(self.board[y][x] == 0):
                return "0"
            else:
                return str(self.board[y][x])
