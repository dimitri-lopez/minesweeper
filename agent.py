#!/usr/bin/env python3
from enums import *
import pickle


THRESHOLD = 0.4
Z_SCORE = 2.576
def sortOnValue(item):
    itemType = 2
    if(item.action == "flag"):
        itemType = 1
    return (abs(item.value), itemType)

def accountForRotation(y, x, rotation):
    for i in range(4 - rotation):
        # temp = y # this is a clockwise rotation
        # y = -x
        # x = temp
        temp = y # this is a counter clockwise rotation
        y = x
        x = -temp
    return(y, x)

def rotate_clockwise(board):
    output = [[0 for i in range(3)] for j in range(3)]
    for x in range(3):
        for y in range(3):
            output[y][x] = board[2 - x][y]
    return output

def boardToString(board):
    output = ""
    for y in range(3):
        for x in range(3):
            output += str(board[y][x])
        output += "|"
    return output

def miniToString(miniBoard):
    outputs = ["", "", "", ""]
    outputs[0] = boardToString(miniBoard)
    for i in range(3):
        miniBoard = rotate_clockwise(miniBoard)
        outputs[i + 1] = boardToString(miniBoard)

    return outputs


class State:
    # 1 is a mine, Flag is -1
    # 9 is a mine in the board, flag is like a 2?
    def __init__(self):
        self.surroundings = [
            0.0, # [ 1,  0]
            0.0, # [ 0,  1]
            0.0, # [-1,  0]
            0.0, # [ 0, -1]
            0.0, # [ 1,  1]
            0.0, # [-1, -1]
            0.0, # [1,  -1]
            0.0, # [-1,  1]
        ]

        self.safeMine = [
            [0, 0], # [ 1,  0]
            [0, 0], # [ 0,  1]
            [0, 0], # [-1,  0]
            [0, 0], # [ 0, -1]
            [0, 0], # [ 1,  1]
            [0, 0], # [-1, -1]
            [0, 0], # [1,  -1]
            [0, 0]  # [-1,  1]
        ]
    def update(self, i):
        safe = self.safeMine[i][0]
        mine = self.safeMine[i][1]
        mean = (mine - safe) / (mine + safe)
        variance_safe = safe*((mean - (-1))**2)
        variance_mine = mine*((mean - ( 1))**2)
        n_minus_one = 1 if (safe + mine - 1 == 0) else (safe + mine - 1)
        variance = (variance_safe + variance_mine) / (n_minus_one)
        bounds = (1.96*(variance/(safe+mine))**0.5)
        if(mean < 0):
            value = mean + bounds
            if value > 0:
                value = 0
        elif(mean == 0):
            value = 0
        else:
            value = mean - bounds
            if value < 0:
                value = 0
        self.surroundings[i] = value

    

    def __repr__(self):
        output = "["
        for i in self.surroundings:
            if i is None:
                output += "{:<5}".format(str(i))
            elif i > 0:
                output += " {:0.2f}".format(i)
            else:
                output += "{:0.2f}".format(i)
            output += ", "
        output += "]"

        output += "   ["
        for i in self.safeMine:
            if i is None:
                output += "{:<6}".format(str(i))
            else:
                output += "({:<3}, {:>3})".format(i[0], i[1])
            output += ", "
        output += "]"
        return output


class Action:
    def __init__(self, action, y, x, value, safeMine):
        self.y = y
        self.x = x
        self.action = action
        self.value = value
        self.safeMine = safeMine
    def __repr__(self):
        output = "{:<8}: ({:<2}, {:>2}) value: {:<4} safeMine: ({})".format(self.action, self.y, self.x, self.value, self.safeMine)
        return output
    def __eq__(self, item):
        if(self.action == item.action and self.y == item.y and self.x == item.x):
            if(abs(self.value) != 1):
                self.value = item.value
            return True
        else:
            return False


class Agent:
    stateMemory = dict()
    toSearch = list() # full of paris of integers (y, x) eg. (1, 1)
    actions = list() #filled with actions
    learningRate = 0.1
    # discount = 0.95 # Not being used atm
    train = True
    visibleBoard = []

    def newGame(self, board, train):
        self.toSearch = list()
        self.actions = list()
        self.board = board
        self.train = train
        self.visibleBoard = [["" for i in range(self.board.cols)] for j in range(self.board.rows)]

        self.actions.append(Action("uncover", self.board.cols // 2, self.board.rows // 2, -2, [0,0]))

    def storeStateMemory(self):
        with open("stateMemory.txt", "wb") as myFile:
            pickle.dump(self.stateMemory, myFile)

    def loadStateMemory(self):
        with open("stateMemory.txt", "rb") as myFile:
            self.stateMemory = pickle.load(myFile)

    def addAction(self, action):
        if(action not in self.actions):
            self.actions.append(action)

    def addToSearch(self, coord):
        if(coord not in self.toSearch):
            self.toSearch.append(coord)

    def getCovered(self): # This only gets called when a guess needs to be made
        y, x = self.board.getCovered()
        self.addAction(Action("uncover", y, x, 0, [0,0]))

    def getAction(self):
        if(len(self.actions) == 0): # If this happens...
            self.getCovered()
        action = self.actions.pop()
        square = self.board.getSquare(action.y, action.x)
        if(self.board.isUncovered(action.y, action.x)): # Get a new action
            return self.getAction()
        return action

    def takeAction(self, debug = False):
        if(len(self.actions) == 0): # No actions left
            self.processSearch()
        elif(abs(self.actions[-1].value) < 1): # Only crappy choices are available
            self.processSearch()

        action = self.getAction()
        y, x = action.y, action.x
        if action.action == "flag": #update surrounding if flag
            for i in surrounding:
                dy = y + i[0]
                dx = x + i[1]
                if(self.board.inBoard(dy, dx) and self.board.isNumber(dy, dx)):
                    self.addToSearch((dy, dx))

            if(debug):
                print("Solver's Move: Flagging: ({:<2}, {:>2})".format(y, x))
            return self.board.flag(y, x)
        elif action.action == "uncover":
            if(debug):
                print("Solver's Move: Uncover: ({:<2}, {:>2})".format(y, x))
            return self.board.move(y, x, self)

    # def processFlags(self, miniBoard):
    #     # Process flags first
    #     for i in surrounding:
    #         dy = 1 + i[0]
    #         dx = 1 + i[1]
    #         if(miniBoard[dy][dx] == "F"):
    #             for i in surrounding:
    #                 dy2 = dy + i[0]
    #                 dx2 = dx + i[1]
    #                 if(dy2 > 2 or dy2 < 0 or dx2 > 2 or dx2 < 0):
    #                     continue
    #                 if(miniBoard[dy2][dx2].isnumeric()):
    #                     miniBoard[dy2][dx2] = int(miniBoard[dy2][dx2]) - 1
    #                     if(miniBoard[dy2][dx2] < 0):
    #                         miniBoard[dy2][dx2] = 0

    #                     miniBoard[dy2][dx2] = str(miniBoard[dy2][dx2])
    #             miniBoard[dy][dx] = "0"
    #     return miniBoard

    # This will push a set of actions onto the queue
    def searchHashTable(self, miniBoard, y, x):
        strings = miniToString(miniBoard)

        found = False
        rotation = 0
        for i in range(len(strings)): # Only get the first orientation from the hashtable
            key = strings[i]
            if(key in self.stateMemory):
                found = True
                rotation = i

        rotationString = strings[rotation]
        state = State()
        if(rotationString in self.stateMemory): # Been seen before
            state = self.stateMemory.get(rotationString)

        # if(y == 9 and x == 1):
        #     print(miniBoard)
        #     print(rotationString)
        #     print(state)
        #     input("heeere")
        # Grab the correct stuff...
        for i in range(len(state.surroundings)):
            value = state.surroundings[i]
            yOffset = surrounding[i][0]
            xOffset = surrounding[i][1]

            yOffset, xOffset = accountForRotation(yOffset, xOffset, rotation)
            dy = y + yOffset
            dx = x + xOffset
            ay = 1 + yOffset
            ax = 1 + xOffset

            if(value is None or miniBoard[ay][ax] != "."): # Number square
                # print("Heere, {}   {}".format(a, b))
                state.surroundings[i] = None
                continue

# .10 | 1.000, None  , None  ,
# .21 |-1.000,         None
# 0.0 |  None, 1.000, None  , ]
            if(self.train == True):
                if(self.board.isMine(dy, dx)): # Found a mine
                    state.safeMine[i][1] += 1
                else:
                    state.safeMine[i][0] += 1
                state.update(i)

            if(value > 0):
                self.addAction(Action("flag", dy, dx, value, state.safeMine[i]))
            elif(value < 0):
                self.addAction(Action("uncover", dy, dx, value, state.safeMine))

        self.stateMemory[rotationString] = state # update dictionary

    def accountForFlags(self):
        flagList = list()
        for y in range(self.board.cols):
            for x in range(self.board.rows):
                piece = self.board.getSquare(y, x)
                self.visibleBoard[y][x] = piece
                if piece == "F":
                    flagList.append((y,x))
        for flagLoc in flagList:
            y = flagLoc[0]
            x = flagLoc[1]
            for i in surrounding:
                dy = y + i[0]
                dx = x + i[1]
                if(self.board.notInBoard(dy, dx)):
                    continue
                if(self.visibleBoard[dy][dx].isnumeric()):
                    self.visibleBoard[dy][dx] = int(self.visibleBoard[dy][dx]) - 1
                    if(self.visibleBoard[dy][dx] < 0):
                        self.visibleBoard[dy][dx] = 0

                    self.visibleBoard[dy][dx] = str(self.visibleBoard[dy][dx])
            self.visibleBoard[y][x] = "0" # Set Flag to zero

    def printBoard(self):
        for y in range(self.board.cols):
            for x in range(self.board.rows):
                print(self.visibleBoard[y][x], end = "")
            print()


    def processSearch(self):
        if(len(self.toSearch) != 0):
            self.accountForFlags() # Subtract surrounding and set flags equal to zero
        while len(self.toSearch) != 0:
            y, x = self.toSearch.pop()
            miniBoard = [[0 for i in range(3)] for j in range(3)]


            # Copy to miniboard
            miniBoard[1][1] = self.visibleBoard[y][x]
            # miniBoard[1][1] = self.board.getSquare(y, x)
            for i in surrounding:
                dy = y + i[0]
                dx = x + i[1]
                ny = 1 + i[0]
                nx = 1 + i[1]
                if(self.board.notInBoard(dy, dx)):
                    miniBoard[ny][nx] = "x"
                else:
                    miniBoard[ny][nx] = self.visibleBoard[dy][dx]

            if(miniBoard[1][1] == "0"): #Flag nuked this sucker
                for i in surrounding:
                    ny = 1 + i[0]
                    nx = 1 + i[1]
                    if(miniBoard[ny][nx] == "."):
                        dy = y + i[0]
                        dx = x + i[1]
                        self.addAction(Action("uncover", dy, dx, -10, [0, 0]))

                continue

            #Search hashtable
            self.searchHashTable(miniBoard, y, x)
        self.actions = sorted(self.actions, key = sortOnValue)

    def printActions(self):
        print("Actions: ")
        for a in self.actions:
            print(a)
    def printSearch(self):
        print("To Be Searched:")
        for i in self.toSearch:
            print(i)

    def printStateMemory(self):
        print("State memory:")
        for key, value in self.stateMemory.items():
            print(key, ' : ', value)

