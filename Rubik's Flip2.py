#!/usr/bin/env python
# coding: utf-8

# In[62]:


import numpy as np
import random


# In[63]:


# Defining classes

class Operator:
    def _init_(self, row, col):
        self.row = row
        self.col = col


class Move:
    def _init_(self, row, col, flipRow, flipCol, flipToRow, flipToCol, color, value):
        self.row = row
        self.col = col

        self.flipRow = flipRow
        self.flipCol = flipCol
        self.flipToRow = flipToRow
        self.flipToCol = flipToCol

        self.color = color

        self.value = value


class State:
    def _init_(self, cell):
        self.cell = cell


class Tile:
    def _init_(self, tileIndex, tileValue, neighbours):
        self.tileIndex = tileIndex
        self.tileValue = tileValue
        self.neighbours = neighbours


# In[64]:


# Assigning values

BLANK = 0
USER_RED = 1
USER_BLUE = 2

PROGRAM_WHITE = 3
PROGRAM_YELLOW = 4

TIE = 5
MAXEVAL = 1000

operator = Operator()


# In[65]:


cell = [[]]
cell = [[0 for i in range(4)] for i in range(4)]
current_State = State()
current_State.cell = cell


# In[66]:


def print_State(state):

    for i in range(18):
        print("-", end="")
    print()
    for i in range(4):
        for j in range(4):
            if state.cell[i][j] == BLANK:
                print("|   ", end="")
            elif state.cell[i][j] == USER_RED:
                print("| R ", end="")
            elif state.cell[i][j] == USER_BLUE:
                print("| B ", end="")
            elif state.cell[i][j] == PROGRAM_WHITE:
                print("| W ", end="")
            elif state.cell[i][j] == PROGRAM_YELLOW:
                print("| Y ", end="")

        print("|")
        for i in range(18):
            print("-", end="")
        print()


print_State(current_State)


# In[67]:


def isValidMove(state, operator):
    if operator.row > 3 or operator.row < 0 or operator.col > 3 or operator.col < 0:
        return 0

    if state.cell[operator.row][operator.col] == BLANK:
        return 1
    else:
        return 0


def makeMove(state, operator, who):
    if not isValidMove(state, operator):
        return 0
    state.cell[operator.row][operator.col] = who


# In[68]:


# Flippable fucntion- returns true if there is a valid neighbour where you can flip to and also a list of valid neighbours in a list

def isFlippable(state, userType):
    if userType == USER_RED or userType == USER_BLUE:
        value1 = 1
        value2 = 2
    if userType == PROGRAM_YELLOW or userType == PROGRAM_WHITE:
        value1 = 3
        value2 = 4
    array = np.array(state.cell)
    opponent_Tiles1 = np.argwhere(array == value1)
    opponent_Tiles2 = np.argwhere(array == value2)
    opponent_Tiles = np.concatenate((opponent_Tiles1, opponent_Tiles2))

    list_neighbours = []
    for i in opponent_Tiles:

        up = i[0]-1
        down = i[0]+1
        left = i[1]-1
        right = i[1]+1

        neighbours = [[i[0], left], [i[0], right], [up, i[1]], [down, i[1]]]

        # Now check if the neighbors are valid
        valid_Neighbours = []
        for neighbour in neighbours:
            operator.row = neighbour[0]
            operator.col = neighbour[1]
            if isValidMove(state, operator):
                valid_Neighbours.append(neighbour)
                list_neighbours.append(neighbour)

    if len(list_neighbours) != 0:
        return [1, list_neighbours]
    elif len(list_neighbours) == 0:
        return [0]


# In[69]:


def isFlippable_State(state):
    if isFlippable(state, USER_RED)[0] or isFlippable(state, PROGRAM_WHITE)[0]:
        return 1
    else:
        return 0


# In[70]:


# returns true if the user can flip the provided tile to the given new place
# Creates neighbours of given tile and then check if they are valid neighbours to flip and if the given operator is in valid neighbors return true
# fliprow and fliprow are initial positions of tile, operator holds new positions

def isValidFlip(state, tiletoFlip, flipRow, flipCol, operator, userType):
    # check if it's your own tile, if it is return false
    if userType == 1 or userType == 2:
        if tiletoFlip == 1 or tiletoFlip == 2:
            return 0

    if userType == 3 or userType == 4:
        if tiletoFlip == 3 or tiletoFlip == 4:
            return 0

    up = flipRow-1
    down = flipRow+1
    left = flipCol-1
    right = flipCol+1

    neighbours = [[flipRow, left], [flipRow, right],
                  [up, flipCol], [down, flipCol]]

    flipArea = [operator.row, operator.col]

    # Now check if the neighbors are valid
    valid_Neighbours = []
    for neighbour in neighbours:
        operator.row = neighbour[0]
        operator.col = neighbour[1]
        if isValidMove(state, operator):
            valid_Neighbours.append(neighbour)

    if flipArea in valid_Neighbours:
        return 1

    return 0


# In[71]:


# returns true if it is a flippable tile
def isFlippableTile(state, flipRow, flipCol):

    up = flipRow-1
    down = flipRow+1
    left = flipCol-1
    right = flipCol+1

    neighbours = [[flipRow, left], [flipRow, right],
                  [up, flipCol], [down, flipCol]]

    # Now check if the neighbors are valid
    valid_Neighbours = []
    for neighbour in neighbours:
        operator.row = neighbour[0]
        operator.col = neighbour[1]
        if isValidMove(state, operator):
            valid_Neighbours.append(neighbour)

    if len(valid_Neighbours) >= 1:
        return 1
    else:
        return 0


# In[72]:


# returns all possible flips for a tile
def allFlipsTile(state, flipRow, flipCol):

    up = flipRow-1
    down = flipRow+1
    left = flipCol-1
    right = flipCol+1

    neighbours = [[flipRow, left], [flipRow, right],
                  [up, flipCol], [down, flipCol]]

    # Now check if the neighbors are valid
    valid_Neighbours = []
    for neighbour in neighbours:
        operator.row = neighbour[0]
        operator.col = neighbour[1]
        if isValidMove(state, operator):
            valid_Neighbours.append(neighbour)

    return valid_Neighbours


# In[73]:


# gives all opponent's flippable tile i.e. given userType
def opponentTiles(state, userType):
    if userType == USER_RED or userType == USER_BLUE:
        value1 = 1
        value2 = 2
    if userType == PROGRAM_YELLOW or userType == PROGRAM_WHITE:
        value1 = 3
        value2 = 4
    array = np.array(state.cell)
    opponent_Tiles1 = np.argwhere(array == value1)
    opponent_Tiles2 = np.argwhere(array == value2)
    opponent_Tiles = np.concatenate((opponent_Tiles1, opponent_Tiles2))
    return opponent_Tiles


# In[74]:


def opponentFlippableTiles(state, userType):
    oppTiles = opponentTiles(state, userType)

    oppFlipTiles = []
    for opp in oppTiles:

        if(isFlippableTile(state, opp[0], opp[1])):
            oppFlipTiles.append([opp[0], opp[1]])
    return oppFlipTiles


# In[ ]:


# flips a random tile for random player


def randomFlip(state, userType):
    # Flips if the current user who wants to flip is White/Yellow
    if userType == PROGRAM_WHITE or userType == PROGRAM_YELLOW:
        element = 3

        valid_Neighbours = []
        # looking for opponent's tile
        while True:
            randomRow = random.randint(0, 3)
            randomCol = random.randint(0, 3)
            element = state.cell[randomRow][randomCol]

            if element == 1 or element == 2:

                up = randomRow-1
                down = randomRow+1
                left = randomCol-1
                right = randomCol+1

                neighbours = [[randomRow, left], [randomRow, right], [
                    up, randomCol], [down, randomCol]]

                for neighbour in neighbours:
                    operator.row = neighbour[0]
                    operator.col = neighbour[1]
                    if isValidMove(state, operator):
                        valid_Neighbours.append(neighbour)

                if(len(valid_Neighbours) > 0):
                    break

        # Now choosing random neighbor to flip

        randomNeighbourIndex = random.randint(0, len(valid_Neighbours)-1)
        randomNeighbour = valid_Neighbours[randomNeighbourIndex]
        print(randomNeighbour)
        # flipping opposite color to the neighbour space
        if element == 1:
            state.cell[randomNeighbour[0]][randomNeighbour[1]] = 2
            # setting the flipped area to blank
            state.cell[randomRow][randomCol] = 0

        if element == 2:
            state.cell[randomNeighbour[0]][randomNeighbour[1]] = 1
            # setting the flipped area to blank
            state.cell[randomRow][randomCol] = 0

    # if our userType is Red/Blue
    if userType == USER_RED or userType == USER_BLUE:
        element = 1

        valid_Neighbours = []
        # looking for opponent's tile
        while True:
            randomRow = random.randint(0, 3)
            randomCol = random.randint(0, 3)
            element = state.cell[randomRow][randomCol]

            if element == 3 or element == 4:

                # get out of loop if you get other than 1 or 2 and find the neighbour and flip

                up = randomRow-1
                down = randomRow+1
                left = randomCol-1
                right = randomCol+1

                neighbours = [[randomRow, left], [randomRow, right], [
                    up, randomCol], [down, randomCol]]

                for neighbour in neighbours:
                    operator.row = neighbour[0]
                    operator.col = neighbour[1]
                    if isValidMove(state, operator):
                        valid_Neighbours.append(neighbour)

                # print(valid_Neighbours)
                if(len(valid_Neighbours) > 0):
                    break

        # Now choosing random neighbor to flip

        randomNeighbourIndex = random.randint(0, len(valid_Neighbours)-1)
        randomNeighbour = valid_Neighbours[randomNeighbourIndex]
        print(randomNeighbour)
        # flipping opposite color to the neighbour space
        if element == 3:
            state.cell[randomNeighbour[0]][randomNeighbour[1]] = 4
            # setting the flipped area to blank
            state.cell[randomRow][randomCol] = 0

        if element == 4:
            state.cell[randomNeighbour[0]][randomNeighbour[1]] = 3
            # setting the flipped area to blank
            state.cell[randomRow][randomCol] = 0


# In[78]:


# moves the userType you provided
def randomMove(state, userType):
    while True:
        randomRow = random.randint(0, 3)
        randomCol = random.randint(0, 3)
        operator.row = randomRow
        operator.col = randomCol

        if not isValidMove(state, operator):
            randomRow = random.randint(0, 3)
            randomCol = random.randint(0, 3)
            operator.row = randomRow
            operator.col = randomCol
        if isValidMove(state, operator):

            if userType == PROGRAM_WHITE or userType == PROGRAM_WHITE:
                state.cell[operator.row][operator.col] = random.randint(3, 4)
                break
            elif userType == USER_RED or userType == USER_BLUE:
                state.cell[operator.row][operator.col] = random.randint(1, 2)
                break


# In[79]:


# currently returns winning value if the provided userType can't be flipped
def isTerminal(s):

    for line in range(0, 4):
        # check for row completion
        if s.cell[line][0] != BLANK and s.cell[line][0] == s.cell[line][1] and s.cell[line][1] == s.cell[line][2]:
            if not isFlippableTile(current_State, line, 0) and not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2):
                # this will return R,B,W,or Y and thats how we know who won
                return s.cell[line][0]

        if s.cell[line][1] != BLANK and s.cell[line][1] == s.cell[line][2] and s.cell[line][2] == s.cell[line][3]:
            if not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2) and not isFlippableTile(current_State, line, 3):
                return s.cell[line][1]

        # check for column completion
        if s.cell[0][line] != BLANK and s.cell[0][line] == s.cell[1][line] and s.cell[1][line] == s.cell[2][line]:
            if not isFlippableTile(current_State, 0, line) and not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line):
                return s.cell[0][line]

        if s.cell[1][line] != BLANK and s.cell[1][line] == s.cell[2][line] and s.cell[2][line] == s.cell[3][line]:
            if not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line) and not isFlippableTile(current_State, 3, line):
                return s.cell[1][line]

        # Check for diagonal- Total 8 diagonal ways
    if s.cell[2][0] != BLANK and s.cell[2][0] == s.cell[1][1] and s.cell[1][1] == s.cell[0][2]:
        if not isFlippableTile(current_State, 2, 0) and not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 0, 2):
            return s.cell[2][0]

    if s.cell[2][1] != BLANK and s.cell[2][1] == s.cell[1][2] and s.cell[1][2] == s.cell[0][3]:
        if not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 0, 3):
            return s.cell[2][1]

    if s.cell[3][0] != BLANK and s.cell[3][0] == s.cell[2][1] and s.cell[2][1] == s.cell[1][2]:
        if not isFlippableTile(current_State, 3, 0) and not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2):
            return s.cell[3][0]

    if s.cell[3][1] != BLANK and s.cell[3][1] == s.cell[2][2] and s.cell[2][2] == s.cell[1][3]:
        if not isFlippableTile(current_State, 3, 1) and not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 1, 3):
            return s.cell[3][1]

    # Another 4 ways through another side \

    if s.cell[0][1] != BLANK and s.cell[0][1] == s.cell[1][2] and s.cell[1][2] == s.cell[2][3]:
        if not isFlippableTile(current_State, 0, 1) and not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 2, 3):
            return s.cell[0][1]

    if s.cell[0][0] != BLANK and s.cell[0][0] == s.cell[1][1] and s.cell[1][1] == s.cell[2][2]:
        if not isFlippableTile(current_State, 0, 0) and not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2):
            return s.cell[0][0]

    if s.cell[1][1] != BLANK and s.cell[1][1] == s.cell[2][2] and s.cell[2][2] == s.cell[3][3]:
        if not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 3, 3):
            return s.cell[1][1]

    if s.cell[1][0] != BLANK and s.cell[1][0] == s.cell[2][1] and s.cell[2][1] == s.cell[3][2]:
        if not isFlippableTile(current_State, 1, 0) and not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 3, 2):
            return s.cell[1][0]

    # Check for any blanks-- return 0 if anyblanks left and not in winning situation
    for i in range(0, 4):
        for j in range(0, 4):
            if s.cell[i][j] == BLANK:
                return 0

    return TIE


# In[101]:


# Function for flip for human player
# Ask for input to flip- check if it's a valid tile(not your tile), check if you can flip the tile to the given space. if yes flip


def human_flip(turn):
    while True:
        # Make sure you are passing integers
        flipRow = int(
            input("Please tell the row of the tile you want to flip? (Row 1-4): "))-1
        flipCol = int(
            input("Please tell the column of the tile you want to flip? (Row 1-4): "))-1

        # check if it's a flippable tile
        if isFlippableTile(current_State, flipRow, flipCol):

            # check if it's an opponent's tile
            if turn == USER_RED or turn == USER_BLUE:
                if current_State.cell[flipRow][flipCol] == 3 or current_State.cell[flipRow][flipCol] == 4:
                    tiletoFlip = current_State.cell[flipRow][flipCol]
                    break
            elif turn == PROGRAM_WHITE or turn == PROGRAM_YELLOW:
                if current_State.cell[flipRow][flipCol] == 1 or current_State.cell[flipRow][flipCol] == 2:
                    tiletoFlip = current_State.cell[flipRow][flipCol]
                    break

        print("It's not a valid tile, please input another tile to flip!")

    while True:
        flipToRow = int(
            input("Please input the row where you want to flip? (Row 1-4): "))-1
        flipToCol = int(
            input("Please input the column where you want to flip? (Row 1-4): "))-1

        operator.row = flipToRow
        operator.col = flipToCol

        if(isValidFlip(current_State, tiletoFlip, flipRow, flipCol, operator, turn)):
            # if it's a yellow tile, flip to white and vice versa
            if tiletoFlip == 3:
                current_State.cell[flipToRow][flipToCol] = 4
                current_State.cell[flipRow][flipCol] = 0
                break
            elif tiletoFlip == 4:
                current_State.cell[flipToRow][flipToCol] = 3
                current_State.cell[flipRow][flipCol] = 0
                break
            elif tiletoFlip == 1:
                current_State.cell[flipToRow][flipToCol] = 2
                current_State.cell[flipRow][flipCol] = 0
                break
            elif tiletoFlip == 2:
                current_State.cell[flipToRow][flipToCol] = 1
                current_State.cell[flipRow][flipCol] = 0
                break

        else:
            print("Invalid flip, please input again")


# In[102]:


# Human move

# Ask for user imput to move, check if valid move and move
def humanMove_P1():
    while True:
        print("Please input your move:")
        rowMove = int(input("Row (1-4): "))-1
        colMove = int(input("Col (1-4): "))-1

        operator.row = rowMove
        operator.col = colMove

        if isValidMove(current_State, operator):
            break
        print("It's not a valid move, please input another move!")

    while True:
        faceColor = input("Which face do you want to place? (Red/Blue): ")
        if faceColor == "Red":
            userType = USER_RED
            break
        elif faceColor == "Blue":
            userType = USER_BLUE
            break
        else:
            print("Please enter a valid face color!")

    makeMove(current_State, operator, userType)


# In[103]:


def humanMove_P2():
    while True:
        print("Please input your move:")
        rowMove = int(input("Row (1-4): "))-1
        colMove = int(input("Col (1-4): "))-1

        operator.row = rowMove
        operator.col = colMove

        if isValidMove(current_State, operator):
            break
        print("It's not a valid move, please input another move!")

    while True:
        faceColor = input("Which face do you want to place? (White/Yellow): ")
        if faceColor == "White":
            userType = PROGRAM_WHITE
            break
        elif faceColor == "Yellow":
            userType = PROGRAM_YELLOW
            break
        else:
            print("Please enter a valid face color!")

    makeMove(current_State, operator, userType)


# In[104]:


def humanVhuman():
    print("Lets play the game! The first player will be Player 1 and second player will be Player 2")
    print("Player 1 has dice Red/Blue and Player 2 has dice White/Yellow")
    print("Player 1 goes first!")

    print_State(current_State)

    # First move
    turn = 1
    userType = USER_RED
    humanMove_P1()
    turn = 2
    print_State(current_State)

    print()
    print("-------------------------------------------")

    # Play until terminal state
    while True:
        if turn == 1:
            print("It's Player 1's turn")
            userType = USER_RED

            # Check if flippable before asking to flip
            if isFlippable(current_State, PROGRAM_WHITE)[0]:
                human_flip(userType)
            else:
                print("No valid flip available! Just place your tile!")
            print_State(current_State)
            humanMove_P1()
            turn = 2
            print_State(current_State)

        elif turn == 2:
            print("It's Player 2's turn")
            userType = PROGRAM_WHITE

            if isFlippable(current_State, USER_RED)[0]:
                human_flip(userType)
            else:
                print("No valid flip available! Just place your tile!")

            print_State(current_State)
            humanMove_P2()
            turn = 1
            print_State(current_State)

        print()
        print("-------------------------------------------")
        finalResult = isTerminal(current_State)
        if finalResult:
            if finalResult == 1 or finalResult == 2:
                print("Player 1 with dice Red/Blue wins")
            elif finalResult == 3 or finalResult == 4:
                print("Player 2 with dice White/Yellow wins")
            elif finalResult == 5:
                print("TIE!")

        if isTerminal(current_State):
            break


# In[105]:


# Add human vs random functionality
def humanVRandom():

    print("Let's play the game Player 1 vs Random")
    while True:
        choice = int(input("Who should go first? (1=User  2=Random): "))
        if choice == 1:
            turn = USER_RED
            print("You will have Red/Blue dice")
            break
        elif choice == 2:
            turn = PROGRAM_WHITE
            print("Random will have White/Yellow dice")
            break
        else:
            print("Choose again!")
    print_State(current_State)

    c = 0
    while True:

        if turn == USER_RED:
            if c > 0:
                if isFlippable(current_State, PROGRAM_WHITE)[0]:
                    human_flip(turn)
                    print_State(current_State)
                else:
                    print("No valid flip available! Just place your tile!")

            humanMove_P1()
            print_State(current_State)

            turn = PROGRAM_WHITE

        elif turn == PROGRAM_WHITE:

            if c > 0:
                # provide the type of tile you want to flip
                if isFlippable(current_State, USER_RED)[0]:
                    # random flip here
                    # provide your user type and it flips the opposite
                    randomFlip(current_State, PROGRAM_WHITE)
                    print("Random flips.....")
                    print_State(current_State)
                else:
                    print("No valid flip available!")

            # randomMOve here
            randomMove(current_State, PROGRAM_WHITE)
            print("Random moves.....")
            print_State(current_State)

            turn = USER_RED

        c = c+1

        print()
        print("-------------------------------------------")
        finalResult = isTerminal(current_State)
        if finalResult:
            if finalResult == 1 or finalResult == 2:
                print("Player 1 with dice Red/Blue wins!")
            elif finalResult == 3 or finalResult == 4:
                print("Random Player wins!")
            elif finalResult == 5:
                print("TIE!")

        if isTerminal(current_State):
            break


# In[106]:


# undo function
def undo(state, operator):

    state.cell[operator.row][operator.col] = BLANK


# In[107]:


# Evaluation function for Ace

def eval(s):
    for line in range(0, 4):
        # check for row completion
        if s.cell[line][0] != BLANK and s.cell[line][0] == s.cell[line][1] and s.cell[line][1] == s.cell[line][2]:
            if not isFlippableTile(current_State, line, 0) and not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2):
                if s.cell[line][0] == USER_RED or s.cell[line][0] == USER_BLUE:
                    return -10
                elif s.cell[line][0] == PROGRAM_WHITE or s.cell[line][0] == PROGRAM_YELLOW:
                    return 10

        if s.cell[line][1] != BLANK and s.cell[line][1] == s.cell[line][2] and s.cell[line][2] == s.cell[line][3]:
            if not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2) and not isFlippableTile(current_State, line, 3):
                if s.cell[line][1] == USER_RED or s.cell[line][1] == USER_BLUE:
                    return -10
                elif s.cell[line][1] == PROGRAM_WHITE or s.cell[line][1] == PROGRAM_YELLOW:
                    return 10

        # check for column completion
        if s.cell[0][line] != BLANK and s.cell[0][line] == s.cell[1][line] and s.cell[1][line] == s.cell[2][line]:
            if not isFlippableTile(current_State, 0, line) and not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line):
                if s.cell[0][line] == USER_RED or s.cell[0][line] == USER_BLUE:
                    return -10
                elif s.cell[0][line] == PROGRAM_WHITE or s.cell[0][line] == PROGRAM_YELLOW:
                    return 10

        if s.cell[1][line] != BLANK and s.cell[1][line] == s.cell[2][line] and s.cell[2][line] == s.cell[3][line]:
            if not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line) and not isFlippableTile(current_State, 3, line):
                if s.cell[1][line] == USER_RED or s.cell[1][line] == USER_BLUE:
                    return -10
                elif s.cell[1][line] == PROGRAM_WHITE or s.cell[1][line] == PROGRAM_YELLOW:
                    return 10

    # Check for diagonal- Total 8 diagonal ways
    # 4 from one side

    if s.cell[2][0] != BLANK and s.cell[2][0] == s.cell[1][1] and s.cell[1][1] == s.cell[0][2]:
        if not isFlippableTile(current_State, 2, 0) and not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 0, 2):
            if s.cell[2][0] == USER_RED or s.cell[2][0] == USER_BLUE:
                return -10
            elif s.cell[2][0] == PROGRAM_WHITE or s.cell[2][0] == PROGRAM_YELLOW:
                return 10

    if s.cell[2][1] != BLANK and s.cell[2][1] == s.cell[1][2] and s.cell[1][2] == s.cell[0][3]:
        if not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 0, 3):
            if s.cell[2][1] == USER_RED or s.cell[2][1] == USER_BLUE:
                return -10
            elif s.cell[2][1] == PROGRAM_WHITE or s.cell[2][1] == PROGRAM_YELLOW:
                return 10

    if s.cell[3][0] != BLANK and s.cell[3][0] == s.cell[2][1] and s.cell[2][1] == s.cell[1][2]:
        if not isFlippableTile(current_State, 3, 0) and not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2):
            if s.cell[3][0] == USER_RED or s.cell[3][0] == USER_BLUE:
                return -10
            elif s.cell[3][0] == PROGRAM_WHITE or s.cell[3][0] == PROGRAM_YELLOW:
                return 10

    if s.cell[3][1] != BLANK and s.cell[3][1] == s.cell[2][2] and s.cell[2][2] == s.cell[1][3]:
        if not isFlippableTile(current_State, 3, 1) and not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 1, 3):
            if s.cell[3][1] == USER_RED or s.cell[3][1] == USER_BLUE:
                return -10
            elif s.cell[3][1] == PROGRAM_WHITE or s.cell[3][1] == PROGRAM_YELLOW:
                return 10

    # Check for diagonal from other side
    if s.cell[0][1] != BLANK and s.cell[0][1] == s.cell[1][2] and s.cell[1][2] == s.cell[2][3]:
        if not isFlippableTile(current_State, 0, 1) and not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 2, 3):
            if s.cell[0][1] == USER_RED or s.cell[0][1] == USER_BLUE:
                return -10
            elif s.cell[0][1] == PROGRAM_WHITE or s.cell[0][1] == PROGRAM_YELLOW:
                return 10

    if s.cell[0][0] != BLANK and s.cell[0][0] == s.cell[1][1] and s.cell[1][1] == s.cell[2][2]:
        if not isFlippableTile(current_State, 0, 0) and not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2):
            if s.cell[0][0] == USER_RED or s.cell[0][0] == USER_BLUE:
                return -10
            elif s.cell[0][0] == PROGRAM_WHITE or s.cell[0][0] == PROGRAM_YELLOW:
                return 10

    if s.cell[1][1] != BLANK and s.cell[1][1] == s.cell[2][2] and s.cell[2][2] == s.cell[3][3]:
        if not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 3, 3):
            if s.cell[1][1] == USER_RED or s.cell[1][1] == USER_BLUE:
                return -10
            elif s.cell[1][1] == PROGRAM_WHITE or s.cell[1][1] == PROGRAM_YELLOW:
                return 10

    if s.cell[1][0] != BLANK and s.cell[1][0] == s.cell[2][1] and s.cell[2][1] == s.cell[3][2]:
        if not isFlippableTile(current_State, 1, 0) and not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 3, 2):
            if s.cell[1][0] == USER_RED or s.cell[1][0] == USER_BLUE:
                return -10
            elif s.cell[1][0] == PROGRAM_WHITE or s.cell[1][0] == PROGRAM_YELLOW:
                return 10

    # Draw condition
    result = isTerminal(s)
    if result == 5:
        return 7

    return 0


# In[108]:


# Evaluation function(same as above) for Ace when it is Red/Blue(just color change)

def eval3(s):
    for line in range(0, 4):
        # check for row completion
        if s.cell[line][0] != BLANK and s.cell[line][0] == s.cell[line][1] and s.cell[line][1] == s.cell[line][2]:
            if not isFlippableTile(current_State, line, 0) and not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2):
                if s.cell[line][0] == USER_RED or s.cell[line][0] == USER_BLUE:
                    return 10
                elif s.cell[line][0] == PROGRAM_WHITE or s.cell[line][0] == PROGRAM_YELLOW:
                    return -10

        if s.cell[line][1] != BLANK and s.cell[line][1] == s.cell[line][2] and s.cell[line][2] == s.cell[line][3]:
            if not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2) and not isFlippableTile(current_State, line, 3):
                if s.cell[line][1] == USER_RED or s.cell[line][1] == USER_BLUE:
                    return 10
                elif s.cell[line][1] == PROGRAM_WHITE or s.cell[line][1] == PROGRAM_YELLOW:
                    return -10

        # check for column completion
        if s.cell[0][line] != BLANK and s.cell[0][line] == s.cell[1][line] and s.cell[1][line] == s.cell[2][line]:
            if not isFlippableTile(current_State, 0, line) and not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line):
                if s.cell[0][line] == USER_RED or s.cell[0][line] == USER_BLUE:
                    return 10
                elif s.cell[0][line] == PROGRAM_WHITE or s.cell[0][line] == PROGRAM_YELLOW:
                    return -10

        if s.cell[1][line] != BLANK and s.cell[1][line] == s.cell[2][line] and s.cell[2][line] == s.cell[3][line]:
            if not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line) and not isFlippableTile(current_State, 3, line):
                if s.cell[1][line] == USER_RED or s.cell[1][line] == USER_BLUE:
                    return 10
                elif s.cell[1][line] == PROGRAM_WHITE or s.cell[1][line] == PROGRAM_YELLOW:
                    return -10

    # Check for diagonal- Total 8 diagonal ways
    # 4 from one side

    if s.cell[2][0] != BLANK and s.cell[2][0] == s.cell[1][1] and s.cell[1][1] == s.cell[0][2]:
        if not isFlippableTile(current_State, 2, 0) and not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 0, 2):
            if s.cell[2][0] == USER_RED or s.cell[2][0] == USER_BLUE:
                return 10
            elif s.cell[2][0] == PROGRAM_WHITE or s.cell[2][0] == PROGRAM_YELLOW:
                return -10

    if s.cell[2][1] != BLANK and s.cell[2][1] == s.cell[1][2] and s.cell[1][2] == s.cell[0][3]:
        if not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 0, 3):
            if s.cell[2][1] == USER_RED or s.cell[2][1] == USER_BLUE:
                return 10
            elif s.cell[2][1] == PROGRAM_WHITE or s.cell[2][1] == PROGRAM_YELLOW:
                return -10

    if s.cell[3][0] != BLANK and s.cell[3][0] == s.cell[2][1] and s.cell[2][1] == s.cell[1][2]:
        if not isFlippableTile(current_State, 3, 0) and not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2):
            if s.cell[3][0] == USER_RED or s.cell[3][0] == USER_BLUE:
                return 10
            elif s.cell[3][0] == PROGRAM_WHITE or s.cell[3][0] == PROGRAM_YELLOW:
                return -10

    if s.cell[3][1] != BLANK and s.cell[3][1] == s.cell[2][2] and s.cell[2][2] == s.cell[1][3]:
        if not isFlippableTile(current_State, 3, 1) and not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 1, 3):
            if s.cell[3][1] == USER_RED or s.cell[3][1] == USER_BLUE:
                return 10
            elif s.cell[3][1] == PROGRAM_WHITE or s.cell[3][1] == PROGRAM_YELLOW:
                return -10

    # Check for diagonal from other side
    if s.cell[0][1] != BLANK and s.cell[0][1] == s.cell[1][2] and s.cell[1][2] == s.cell[2][3]:
        if not isFlippableTile(current_State, 0, 1) and not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 2, 3):
            if s.cell[0][1] == USER_RED or s.cell[0][1] == USER_BLUE:
                return 10
            elif s.cell[0][1] == PROGRAM_WHITE or s.cell[0][1] == PROGRAM_YELLOW:
                return -10

    if s.cell[0][0] != BLANK and s.cell[0][0] == s.cell[1][1] and s.cell[1][1] == s.cell[2][2]:
        if not isFlippableTile(current_State, 0, 0) and not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2):
            if s.cell[0][0] == USER_RED or s.cell[0][0] == USER_BLUE:
                return 10
            elif s.cell[0][0] == PROGRAM_WHITE or s.cell[0][0] == PROGRAM_YELLOW:
                return -10

    if s.cell[1][1] != BLANK and s.cell[1][1] == s.cell[2][2] and s.cell[2][2] == s.cell[3][3]:
        if not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 3, 3):
            if s.cell[1][1] == USER_RED or s.cell[1][1] == USER_BLUE:
                return 10
            elif s.cell[1][1] == PROGRAM_WHITE or s.cell[1][1] == PROGRAM_YELLOW:
                return -10

    if s.cell[1][0] != BLANK and s.cell[1][0] == s.cell[2][1] and s.cell[2][1] == s.cell[3][2]:
        if not isFlippableTile(current_State, 1, 0) and not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 3, 2):
            if s.cell[1][0] == USER_RED or s.cell[1][0] == USER_BLUE:
                return 10
            elif s.cell[1][0] == PROGRAM_WHITE or s.cell[1][0] == PROGRAM_YELLOW:
                return -10

    result = isTerminal(s)
    if result == 5:
        return 7

    return 0


# In[109]:


# Evaluation function for Bob(AI-2)

def eval2(s):
    for line in range(0, 4):
        # check for row completion
        if s.cell[line][0] != BLANK and s.cell[line][0] == s.cell[line][1] and s.cell[line][1] == s.cell[line][2]:
            if not isFlippableTile(current_State, line, 0) and not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2):
                if s.cell[line][0] == USER_RED or s.cell[line][0] == USER_BLUE:
                    return -10
                elif s.cell[line][0] == PROGRAM_WHITE or s.cell[line][0] == PROGRAM_YELLOW:
                    return 10

        if s.cell[line][1] != BLANK and s.cell[line][1] == s.cell[line][2] and s.cell[line][2] == s.cell[line][3]:
            if not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2) and not isFlippableTile(current_State, line, 3):
                if s.cell[line][1] == USER_RED or s.cell[line][1] == USER_BLUE:
                    return -10
                elif s.cell[line][1] == PROGRAM_WHITE or s.cell[line][1] == PROGRAM_YELLOW:
                    return 10

        # check for column completion
        if s.cell[0][line] != BLANK and s.cell[0][line] == s.cell[1][line] and s.cell[1][line] == s.cell[2][line]:
            if not isFlippableTile(current_State, 0, line) and not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line):
                if s.cell[0][line] == USER_RED or s.cell[0][line] == USER_BLUE:
                    return -10
                elif s.cell[0][line] == PROGRAM_WHITE or s.cell[0][line] == PROGRAM_YELLOW:
                    return 10

        if s.cell[1][line] != BLANK and s.cell[1][line] == s.cell[2][line] and s.cell[2][line] == s.cell[3][line]:
            if not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line) and not isFlippableTile(current_State, 3, line):
                if s.cell[1][line] == USER_RED or s.cell[1][line] == USER_BLUE:
                    return -10
                elif s.cell[1][line] == PROGRAM_WHITE or s.cell[1][line] == PROGRAM_YELLOW:
                    return 10

    # Check for diagonal- Total 8 diagonal ways
    # 4 from one side

    if s.cell[2][0] != BLANK and s.cell[2][0] == s.cell[1][1] and s.cell[1][1] == s.cell[0][2]:
        if not isFlippableTile(current_State, 2, 0) and not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 0, 2):
            if s.cell[2][0] == USER_RED or s.cell[2][0] == USER_BLUE:
                return -10
            elif s.cell[2][0] == PROGRAM_WHITE or s.cell[2][0] == PROGRAM_YELLOW:
                return 10

    if s.cell[2][1] != BLANK and s.cell[2][1] == s.cell[1][2] and s.cell[1][2] == s.cell[0][3]:
        if not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 0, 3):
            if s.cell[2][1] == USER_RED or s.cell[2][1] == USER_BLUE:
                return -10
            elif s.cell[2][1] == PROGRAM_WHITE or s.cell[2][1] == PROGRAM_YELLOW:
                return 10

    if s.cell[3][0] != BLANK and s.cell[3][0] == s.cell[2][1] and s.cell[2][1] == s.cell[1][2]:
        if not isFlippableTile(current_State, 3, 0) and not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2):
            if s.cell[3][0] == USER_RED or s.cell[3][0] == USER_BLUE:
                return -10
            elif s.cell[3][0] == PROGRAM_WHITE or s.cell[3][0] == PROGRAM_YELLOW:
                return 10

    if s.cell[3][1] != BLANK and s.cell[3][1] == s.cell[2][2] and s.cell[2][2] == s.cell[1][3]:
        if not isFlippableTile(current_State, 3, 1) and not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 1, 3):
            if s.cell[3][1] == USER_RED or s.cell[3][1] == USER_BLUE:
                return -10
            elif s.cell[3][1] == PROGRAM_WHITE or s.cell[3][1] == PROGRAM_YELLOW:
                return 10

    # Check for diagonal from other side
    if s.cell[0][1] != BLANK and s.cell[0][1] == s.cell[1][2] and s.cell[1][2] == s.cell[2][3]:
        if not isFlippableTile(current_State, 0, 1) and not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 2, 3):
            if s.cell[0][1] == USER_RED or s.cell[0][1] == USER_BLUE:
                return -10
            elif s.cell[0][1] == PROGRAM_WHITE or s.cell[0][1] == PROGRAM_YELLOW:
                return 10

    if s.cell[0][0] != BLANK and s.cell[0][0] == s.cell[1][1] and s.cell[1][1] == s.cell[2][2]:
        if not isFlippableTile(current_State, 0, 0) and not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2):
            if s.cell[0][0] == USER_RED or s.cell[0][0] == USER_BLUE:
                return -10
            elif s.cell[0][0] == PROGRAM_WHITE or s.cell[0][0] == PROGRAM_YELLOW:
                return 10

    if s.cell[1][1] != BLANK and s.cell[1][1] == s.cell[2][2] and s.cell[2][2] == s.cell[3][3]:
        if not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 3, 3):
            if s.cell[1][1] == USER_RED or s.cell[1][1] == USER_BLUE:
                return -10
            elif s.cell[1][1] == PROGRAM_WHITE or s.cell[1][1] == PROGRAM_YELLOW:
                return 10

    if s.cell[1][0] != BLANK and s.cell[1][0] == s.cell[2][1] and s.cell[2][1] == s.cell[3][2]:
        if not isFlippableTile(current_State, 1, 0) and not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 3, 2):
            if s.cell[1][0] == USER_RED or s.cell[1][0] == USER_BLUE:
                return -10
            elif s.cell[1][0] == PROGRAM_WHITE or s.cell[1][0] == PROGRAM_YELLOW:
                return 10

    # Other cases

    for line in range(0, 4):
        # check for row
        if s.cell[line][0] != BLANK and s.cell[line][0] == s.cell[line][1]:
            if not isFlippableTile(current_State, line, 0) and not isFlippableTile(current_State, line, 1):
                if s.cell[line][0] == USER_RED or s.cell[line][0] == USER_BLUE:
                    return -3
                elif s.cell[line][0] == PROGRAM_WHITE or s.cell[line][0] == PROGRAM_YELLOW:
                    return 3

        if s.cell[line][1] != BLANK and s.cell[line][1] == s.cell[line][2]:
            if not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2):
                if s.cell[line][1] == USER_RED or s.cell[line][1] == USER_BLUE:
                    return -3
                elif s.cell[line][1] == PROGRAM_WHITE or s.cell[line][1] == PROGRAM_YELLOW:
                    return 3

        if s.cell[line][2] != BLANK and s.cell[line][2] == s.cell[line][3]:
            if not isFlippableTile(current_State, line, 1) and not isFlippableTile(current_State, line, 2):
                if s.cell[line][2] == USER_RED or s.cell[line][2] == USER_BLUE:
                    return -3
                elif s.cell[line][2] == PROGRAM_WHITE or s.cell[line][2] == PROGRAM_YELLOW:
                    return 3

        # check for column
        if s.cell[0][line] != BLANK and s.cell[0][line] == s.cell[1][line]:
            if not isFlippableTile(current_State, 0, line) and not isFlippableTile(current_State, 1, line):
                if s.cell[0][line] == USER_RED or s.cell[0][line] == USER_BLUE:
                    return -3
                elif s.cell[0][line] == PROGRAM_WHITE or s.cell[0][line] == PROGRAM_YELLOW:
                    return 3

        if s.cell[1][line] != BLANK and s.cell[1][line] == s.cell[2][line]:
            if not isFlippableTile(current_State, 1, line) and not isFlippableTile(current_State, 2, line):
                if s.cell[1][line] == USER_RED or s.cell[1][line] == USER_BLUE:
                    return -3
                elif s.cell[1][line] == PROGRAM_WHITE or s.cell[1][line] == PROGRAM_YELLOW:
                    return 3

        if s.cell[2][line] != BLANK and s.cell[2][line] == s.cell[3][line]:
            if not isFlippableTile(current_State, 2, line) and not isFlippableTile(current_State, 3, line):
                if s.cell[2][line] == USER_RED or s.cell[2][line] == USER_BLUE:
                    return -3
                elif s.cell[2][line] == PROGRAM_WHITE or s.cell[2][line] == PROGRAM_YELLOW:
                    return 3

    # for Bob
    if s.cell[2][0] != BLANK and s.cell[2][0] == s.cell[1][1]:
        if not isFlippableTile(current_State, 2, 0) and not isFlippableTile(current_State, 1, 1):
            if s.cell[2][0] == USER_RED or s.cell[1][1] == USER_BLUE:
                return -3
            elif s.cell[2][0] == PROGRAM_WHITE or s.cell[1][1] == PROGRAM_YELLOW:
                return 3

    if s.cell[1][1] != BLANK and s.cell[1][1] == s.cell[0][2]:
        if not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 0, 2):
            if s.cell[1][1] == USER_RED or s.cell[0][2] == USER_BLUE:
                return -3
            elif s.cell[1][1] == PROGRAM_WHITE or s.cell[0][2] == PROGRAM_YELLOW:
                return 3

    if s.cell[2][1] != BLANK and s.cell[2][1] == s.cell[1][2]:
        if not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2):
            if s.cell[2][1] == USER_RED or s.cell[1][2] == USER_BLUE:
                return -3
            elif s.cell[2][1] == PROGRAM_WHITE or s.cell[1][2] == PROGRAM_YELLOW:
                return 3

    if s.cell[1][2] != BLANK and s.cell[1][2] == s.cell[0][3]:
        if not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 0, 3):
            if s.cell[1][2] == USER_RED or s.cell[0][3] == USER_BLUE:
                return -3
            elif s.cell[1][2] == PROGRAM_WHITE or s.cell[0][3] == PROGRAM_YELLOW:
                return 3

    if s.cell[3][0] != BLANK and s.cell[3][0] == s.cell[2][1]:
        if not isFlippableTile(current_State, 3, 0) and not isFlippableTile(current_State, 2, 1):
            if s.cell[3][0] == USER_RED or s.cell[2][1] == USER_BLUE:
                return -3
            elif s.cell[3][0] == PROGRAM_WHITE or s.cell[2][1] == PROGRAM_YELLOW:
                return 3

    if s.cell[2][1] != BLANK and s.cell[2][1] == s.cell[1][2]:
        if not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 1, 2):
            if s.cell[2][1] == USER_RED or s.cell[1][2] == USER_BLUE:
                return -3
            elif s.cell[2][1] == PROGRAM_WHITE or s.cell[1][2] == PROGRAM_YELLOW:
                return 3

    if s.cell[3][1] != BLANK and s.cell[3][1] == s.cell[2][2]:
        if not isFlippableTile(current_State, 3, 1) and not isFlippableTile(current_State, 2, 2):
            if s.cell[3][1] == USER_RED or s.cell[3][1] == USER_BLUE:
                return -3
            elif s.cell[3][1] == PROGRAM_WHITE or s.cell[3][1] == PROGRAM_YELLOW:
                return 3

    if s.cell[2][2] != BLANK and s.cell[2][2] == s.cell[1][3]:
        if not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 1, 3):
            if s.cell[2][2] == USER_RED or s.cell[2][2] == USER_BLUE:
                return -3
            elif s.cell[2][2] == PROGRAM_WHITE or s.cell[2][2] == PROGRAM_YELLOW:
                return 3

    # Another 4 ways through another side \

    if s.cell[0][1] != BLANK and s.cell[0][1] == s.cell[1][2]:
        if not isFlippableTile(current_State, 0, 1) and not isFlippableTile(current_State, 1, 2):
            if s.cell[0][1] == USER_RED or s.cell[0][1] == USER_BLUE:
                return -3
            elif s.cell[0][1] == PROGRAM_WHITE or s.cell[0][1] == PROGRAM_YELLOW:
                return 3

    if s.cell[1][2] != BLANK and s.cell[1][2] == s.cell[2][3]:
        if not isFlippableTile(current_State, 1, 2) and not isFlippableTile(current_State, 2, 3):
            if s.cell[1][2] == USER_RED or s.cell[1][2] == USER_BLUE:
                return -3
            elif s.cell[1][2] == PROGRAM_WHITE or s.cell[2][3] == PROGRAM_YELLOW:
                return 3

    if s.cell[0][0] != BLANK and s.cell[0][0] == s.cell[1][1]:
        if not isFlippableTile(current_State, 0, 0) and not isFlippableTile(current_State, 1, 1):
            if s.cell[0][0] == USER_RED or s.cell[0][0] == USER_BLUE:
                return -3
            elif s.cell[0][0] == PROGRAM_WHITE or s.cell[0][0] == PROGRAM_YELLOW:
                return 3

    if s.cell[1][1] != BLANK and s.cell[1][1] == s.cell[2][2]:
        if not isFlippableTile(current_State, 1, 1) and not isFlippableTile(current_State, 2, 2):
            if s.cell[1][1] == USER_RED or s.cell[1][1] == USER_BLUE:
                return -3
            elif s.cell[1][1] == PROGRAM_WHITE or s.cell[1][1] == PROGRAM_YELLOW:
                return 3

    if s.cell[2][2] != BLANK and s.cell[2][2] == s.cell[3][3]:
        if not isFlippableTile(current_State, 2, 2) and not isFlippableTile(current_State, 3, 3):
            if s.cell[2][2] == USER_RED or s.cell[2][2] == USER_BLUE:
                return -3
            elif s.cell[2][2] == PROGRAM_WHITE or s.cell[2][2] == PROGRAM_YELLOW:
                return 3

    if s.cell[1][0] != BLANK and s.cell[1][0] == s.cell[2][1]:
        if not isFlippableTile(current_State, 1, 0) and not isFlippableTile(current_State, 2, 1):
            if s.cell[1][0] == USER_RED or s.cell[1][0] == USER_BLUE:
                return -3
            elif s.cell[1][0] == PROGRAM_WHITE or s.cell[1][0] == PROGRAM_YELLOW:
                return 3

    if s.cell[2][1] != BLANK and s.cell[2][1] == s.cell[3][2]:
        if not isFlippableTile(current_State, 2, 1) and not isFlippableTile(current_State, 3, 2):
            if s.cell[2][1] == USER_RED or s.cell[2][1] == USER_BLUE:
                return -3
            elif s.cell[2][1] == PROGRAM_WHITE or s.cell[2][1] == PROGRAM_YELLOW:
                return 3

    # Write a draw condition(change it for both user + and -)
    result = isTerminal(s)
    if result == 5:
        return 2

    return 0


# In[110]:


# Max and min fucntions

maxDepth = 2


def max(s, depth, alpha, beta):
    m = Move()
    bestmove = Move()
    operatorAI = Operator()
    colorType = [PROGRAM_WHITE, PROGRAM_YELLOW]

    if depth == maxDepth or isTerminal(s):
        m.value = eval(s)
        return m

    bestmove.value = alpha

    # check if flippable too
    if isFlippable(s, USER_RED)[0]:
        opponentFlipTiles = opponentFlippableTiles(s, USER_RED)
        for tile in opponentFlipTiles:
            element = current_State.cell[tile[0]][tile[1]]

            flipRow = tile[0]
            flipCol = tile[1]

            allFlips = allFlipsTile(s, flipRow, flipCol)

            for i in range(len(allFlips)):
                flipToRow = allFlips[i][0]
                flipToCol = allFlips[i][1]

                if element == 1:
                    s.cell[flipToRow][flipToCol] = 2
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                elif element == 2:
                    s.cell[flipToRow][flipToCol] = 1
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                for i in range(4):
                    for j in range(4):
                        # this is just for moves
                        operatorAI.row = i
                        operatorAI.col = j

                        if i == flipToRow and j == flipToCol:
                            continue

                        if isValidMove(s, operatorAI):

                            for moveColor in colorType:
                                makeMove(s, operatorAI, moveColor)
                                m = min(s, depth+1, bestmove.value, beta)

                                # undo move
                                undo(s, operatorAI)

                                # undo flip
                                s.cell[flipRow][flipCol] = element
                                s.cell[flipToRow][flipToCol] = 0

                                if(m.value > bestmove.value):
                                    bestmove.value = m.value

                                    #bestmove.color and flip
                                    bestmove.row = i
                                    bestmove.col = j

                                    bestmove.color = moveColor

                                    bestmove.flipRow = flipRow
                                    bestmove.flipCol = flipCol

                                    bestmove.flipToRow = flipToRow
                                    bestmove.flipToCol = flipToCol
            #                         print(moveColor)

                                    if m.value > beta:
                                        bestmove.value = beta
                                        return bestmove

#         return bestmove
    else:
        #         print("a2")
        for i in range(4):
            for j in range(4):
                # this is just for moves
                operatorAI.row = i
                operatorAI.col = j

                if isValidMove(s, operatorAI):

                    for moveColor in colorType:
                        makeMove(s, operatorAI, moveColor)
                        m = min(s, depth+1, bestmove.value, beta)

                        # undo move
                        undo(s, operatorAI)

    #                                         print(moveColor)

                        if(m.value > bestmove.value):
                            bestmove.value = m.value

                            #bestmove.color and flip
                            bestmove.row = i
                            bestmove.col = j

                            bestmove.color = moveColor

                            if m.value > beta:
                                bestmove.value = beta
                                return bestmove

    return bestmove


# Min function
def min(s, depth, alpha, beta):

    # may be change these names...
    m = Move()  # Also include best flip
    bestmove = Move()
    operatorAI = Operator()
    colorType = [USER_BLUE, USER_RED]

    if depth == maxDepth or isTerminal(s):
        m.value = eval(s)
        return m

    bestmove.value = beta

    if isFlippable(s, PROGRAM_WHITE)[0]:
        opponentFlipTiles = opponentFlippableTiles(s, PROGRAM_WHITE)
        for tile in opponentFlipTiles:
            element = current_State.cell[tile[0]][tile[1]]

            flipRow = tile[0]
            flipCol = tile[1]

            allFlips = allFlipsTile(s, flipRow, flipCol)

            for i in range(len(allFlips)):
                flipToRow = allFlips[i][0]
                flipToCol = allFlips[i][1]

                if element == 3:
                    s.cell[flipToRow][flipToCol] = 4
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                elif element == 4:
                    s.cell[flipToRow][flipToCol] = 3
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                for i in range(4):
                    for j in range(4):
                        # this is just for moves
                        operatorAI.row = i
                        operatorAI.col = j

                        if i == flipToRow and j == flipToCol:
                            continue

                        if isValidMove(s, operatorAI):

                            # for both colors

                            for moveColor in colorType:
                                makeMove(s, operatorAI, moveColor)
                                m = max(s, depth+1, alpha, bestmove.value)

                                # undo move
                                undo(s, operatorAI)

                                # undo flip
                                s.cell[flipRow][flipCol] = element
                                s.cell[flipToRow][flipToCol] = 0

    #                                             print(moveColor)

                                if(m.value < bestmove.value):
                                    bestmove.value = m.value

                                    #bestmove.color and flip
                                    bestmove.row = i
                                    bestmove.col = j

                                    bestmove.color = moveColor

                                    bestmove.flipRow = flipRow
                                    bestmove.flipCol = flipCol

                                    bestmove.flipToRow = flipToRow
                                    bestmove.flipToCol = flipToCol
    #                                                 print(moveColor)

                                    if m.value < alpha:
                                        bestmove.value = alpha
                                        return bestmove

    else:
        #         print("a4")
        for i in range(4):
            for j in range(4):
                # this is just for moves
                operatorAI.row = i
                operatorAI.col = j

                if isValidMove(s, operatorAI):

                    #                 print("ayo2")
                    for moveColor in colorType:
                        makeMove(s, operatorAI, moveColor)

                        m = max(s, depth+1, alpha, bestmove.value)

                        # undo move
                        undo(s, operatorAI)
        #                 print("ayo5")
                        if(m.value < bestmove.value):
                            bestmove.value = m.value

                            #bestmove.color and flip
                            bestmove.row = i
                            bestmove.col = j

                            bestmove.color = moveColor

                            if m.value < alpha:
                                bestmove.value = alpha
                                return bestmove

    return bestmove


# In[111]:


# For Ace when it takes Red/Blue dice


def max3(s, depth, alpha, beta):
    m = Move()  # Also include best flip
    bestmove = Move()
    operatorAI = Operator()
    colorType = [USER_RED, USER_BLUE]

    if depth == maxDepth or isTerminal(s):
        m.value = eval3(s)
        return m

    bestmove.value = alpha

    # check if flippable too
    if isFlippable(s, PROGRAM_WHITE)[0]:
        opponentFlipTiles = opponentFlippableTiles(s, PROGRAM_WHITE)
        for tile in opponentFlipTiles:
            element = current_State.cell[tile[0]][tile[1]]

            flipRow = tile[0]
            flipCol = tile[1]

            allFlips = allFlipsTile(s, flipRow, flipCol)

            for i in range(len(allFlips)):
                flipToRow = allFlips[i][0]
                flipToCol = allFlips[i][1]

                if element == 3:
                    s.cell[flipToRow][flipToCol] = 4
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                elif element == 4:
                    s.cell[flipToRow][flipToCol] = 3
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                for i in range(4):
                    for j in range(4):
                        # this is just for moves
                        operatorAI.row = i
                        operatorAI.col = j

                        if i == flipToRow and j == flipToCol:
                            continue

                        if isValidMove(s, operatorAI):

                            # for both colors

                            for moveColor in colorType:
                                makeMove(s, operatorAI, moveColor)
                                m = min3(s, depth+1, bestmove.value, beta)

                                # undo move
                                undo(s, operatorAI)

                                # undo flip
                                s.cell[flipRow][flipCol] = element
                                s.cell[flipToRow][flipToCol] = 0

                                if(m.value > bestmove.value):
                                    bestmove.value = m.value

                                    #bestmove.color and flip
                                    bestmove.row = i
                                    bestmove.col = j

                                    bestmove.color = moveColor

                                    bestmove.flipRow = flipRow
                                    bestmove.flipCol = flipCol

                                    bestmove.flipToRow = flipToRow
                                    bestmove.flipToCol = flipToCol

                                    if m.value > beta:
                                        bestmove.value = beta
                                        return bestmove

    else:

        for i in range(4):
            for j in range(4):
                # this is just for moves
                operatorAI.row = i
                operatorAI.col = j

                if isValidMove(s, operatorAI):

                    for moveColor in colorType:
                        makeMove(s, operatorAI, moveColor)
                        m = min3(s, depth+1, bestmove.value, beta)

                        # undo move
                        undo(s, operatorAI)

    #                                         print(moveColor)

                        if(m.value > bestmove.value):
                            bestmove.value = m.value

                            #bestmove.color and flip
                            bestmove.row = i
                            bestmove.col = j

                            bestmove.color = moveColor

                            if m.value > beta:
                                bestmove.value = beta
                                return bestmove

    return bestmove


# Min function
def min3(s, depth, alpha, beta):

    # may be change these names...
    m = Move()  # Also include best flip
    bestmove = Move()
    operatorAI = Operator()
    colorType = [PROGRAM_WHITE, PROGRAM_YELLOW]

    if depth == maxDepth or isTerminal(s):
        m.value = eval3(s)
        return m

    bestmove.value = beta

    if isFlippable(s, USER_RED)[0]:
        opponentFlipTiles = opponentFlippableTiles(s, USER_RED)
        for tile in opponentFlipTiles:
            element = current_State.cell[tile[0]][tile[1]]

            flipRow = tile[0]
            flipCol = tile[1]

            allFlips = allFlipsTile(s, flipRow, flipCol)

            for i in range(len(allFlips)):
                flipToRow = allFlips[i][0]
                flipToCol = allFlips[i][1]

                if element == 1:
                    s.cell[flipToRow][flipToCol] = 2
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                elif element == 2:
                    s.cell[flipToRow][flipToCol] = 1
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                for i in range(4):
                    for j in range(4):
                        # this is just for moves
                        operatorAI.row = i
                        operatorAI.col = j

                        if i == flipToRow and j == flipToCol:
                            continue

                        if isValidMove(s, operatorAI):

                            # for both colors

                            for moveColor in colorType:
                                makeMove(s, operatorAI, moveColor)
                                m = max3(s, depth+1, alpha, bestmove.value)

                                # undo move
                                undo(s, operatorAI)

                                # undo flip
                                s.cell[flipRow][flipCol] = element
                                s.cell[flipToRow][flipToCol] = 0

                                if(m.value < bestmove.value):
                                    bestmove.value = m.value

                                    #bestmove.color and flip
                                    bestmove.row = i
                                    bestmove.col = j

                                    bestmove.color = moveColor

                                    bestmove.flipRow = flipRow
                                    bestmove.flipCol = flipCol

                                    bestmove.flipToRow = flipToRow
                                    bestmove.flipToCol = flipToCol

                                    if m.value < alpha:
                                        bestmove.value = alpha
                                        return bestmove

    else:

        for i in range(4):
            for j in range(4):
                # this is just for moves
                operatorAI.row = i
                operatorAI.col = j

                if isValidMove(s, operatorAI):

                    #                 print("ayo2")
                    for moveColor in colorType:
                        makeMove(s, operatorAI, moveColor)

                        m = max3(s, depth+1, alpha, bestmove.value)

                        # undo move
                        undo(s, operatorAI)
        #                 print("ayo5")
                        if(m.value < bestmove.value):
                            bestmove.value = m.value

                            #bestmove.color and flip
                            bestmove.row = i
                            bestmove.col = j

                            bestmove.color = moveColor

                            if m.value < alpha:
                                bestmove.value = alpha
                                return bestmove

    return bestmove


# In[112]:


# Min and max function For Bob

maxDepth = 2


def max2(s, depth, alpha, beta):
    m = Move()  # Also include best flip
    bestmove = Move()
    operatorAI = Operator()
    colorType = [PROGRAM_WHITE, PROGRAM_YELLOW]

    if depth == maxDepth or isTerminal(s):
        m.value = eval2(s)
        return m

    bestmove.value = alpha

    # check if flippable too
    if isFlippable(s, USER_RED)[0]:
        opponentFlipTiles = opponentFlippableTiles(s, USER_RED)
        for tile in opponentFlipTiles:
            element = current_State.cell[tile[0]][tile[1]]

            flipRow = tile[0]
            flipCol = tile[1]

            allFlips = allFlipsTile(s, flipRow, flipCol)

            for i in range(len(allFlips)):
                flipToRow = allFlips[i][0]
                flipToCol = allFlips[i][1]

                if element == 1:
                    s.cell[flipToRow][flipToCol] = 2
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                elif element == 2:
                    s.cell[flipToRow][flipToCol] = 1
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                for i in range(4):
                    for j in range(4):
                        # this is just for moves
                        operatorAI.row = i
                        operatorAI.col = j

                        if i == flipToRow and j == flipToCol:
                            continue

                        if isValidMove(s, operatorAI):

                            # for both colors

                            for moveColor in colorType:
                                makeMove(s, operatorAI, moveColor)
                                m = min2(s, depth+1, bestmove.value, beta)

                                # undo move
                                undo(s, operatorAI)

                                # undo flip
                                s.cell[flipRow][flipCol] = element
                                s.cell[flipToRow][flipToCol] = 0

                                if(m.value > bestmove.value):
                                    bestmove.value = m.value

                                    #bestmove.color and flip
                                    bestmove.row = i
                                    bestmove.col = j

                                    bestmove.color = moveColor

                                    bestmove.flipRow = flipRow
                                    bestmove.flipCol = flipCol

                                    bestmove.flipToRow = flipToRow
                                    bestmove.flipToCol = flipToCol

                                    if m.value > beta:
                                        bestmove.value = beta
                                        return bestmove

    else:

        for i in range(4):
            for j in range(4):
                # this is just for moves
                operatorAI.row = i
                operatorAI.col = j

                if isValidMove(s, operatorAI):

                    for moveColor in colorType:
                        makeMove(s, operatorAI, moveColor)
                        m = min2(s, depth+1, bestmove.value, beta)

                        # undo move
                        undo(s, operatorAI)

                        if(m.value > bestmove.value):
                            bestmove.value = m.value

                            #bestmove.color and flip
                            bestmove.row = i
                            bestmove.col = j

                            bestmove.color = moveColor

                            if m.value > beta:
                                bestmove.value = beta
                                return bestmove

    return bestmove


# Min function
def min2(s, depth, alpha, beta):

    m = Move()
    bestmove = Move()
    operatorAI = Operator()
    colorType = [USER_BLUE, USER_RED]

    if depth == maxDepth or isTerminal(s):
        m.value = eval2(s)
        return m

    bestmove.value = beta

    if isFlippable(s, PROGRAM_WHITE)[0]:
        opponentFlipTiles = opponentFlippableTiles(s, PROGRAM_WHITE)
        for tile in opponentFlipTiles:
            element = current_State.cell[tile[0]][tile[1]]

            flipRow = tile[0]
            flipCol = tile[1]

            allFlips = allFlipsTile(s, flipRow, flipCol)

            for i in range(len(allFlips)):
                flipToRow = allFlips[i][0]
                flipToCol = allFlips[i][1]

                if element == 3:
                    s.cell[flipToRow][flipToCol] = 4
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                elif element == 4:
                    s.cell[flipToRow][flipToCol] = 3
                    # setting the flipped area to blank
                    s.cell[flipRow][flipCol] = 0

                for i in range(4):
                    for j in range(4):
                        # this is just for moves
                        operatorAI.row = i
                        operatorAI.col = j

                        if i == flipToRow and j == flipToCol:
                            continue

                        if isValidMove(s, operatorAI):

                            # for both colors

                            for moveColor in colorType:
                                makeMove(s, operatorAI, moveColor)
                                m = max2(s, depth+1, alpha, bestmove.value)

                                # undo move
                                undo(s, operatorAI)

                                # undo flip
                                s.cell[flipRow][flipCol] = element
                                s.cell[flipToRow][flipToCol] = 0

                                if(m.value < bestmove.value):
                                    bestmove.value = m.value

                                    #bestmove.color and flip
                                    bestmove.row = i
                                    bestmove.col = j

                                    bestmove.color = moveColor

                                    bestmove.flipRow = flipRow
                                    bestmove.flipCol = flipCol

                                    bestmove.flipToRow = flipToRow
                                    bestmove.flipToCol = flipToCol

                                    if m.value < alpha:
                                        bestmove.value = alpha
                                        return bestmove

    else:

        for i in range(4):
            for j in range(4):
                # this is just for moves
                operatorAI.row = i
                operatorAI.col = j

                if isValidMove(s, operatorAI):

                    for moveColor in colorType:
                        makeMove(s, operatorAI, moveColor)

                        m = max2(s, depth+1, alpha, bestmove.value)

                        # undo move
                        undo(s, operatorAI)

                        if(m.value < bestmove.value):
                            bestmove.value = m.value

                            #bestmove.color and flip
                            bestmove.row = i
                            bestmove.col = j

                            bestmove.color = moveColor

                            if m.value < alpha:
                                bestmove.value = alpha
                                return bestmove

    return bestmove


# In[120]:


# humanVsAI
def humanVAI():

    print("Let's play the game Player 1 vs Ace")
    while True:
        choice = input("Who should go first? (1=User  2=Ace): ")
        if int(choice) == 1:
            turn = USER_RED
            print("You will have Red/Blue dice")
            break
        elif int(choice) == 2:
            turn = PROGRAM_WHITE
            print("Ace will have White/Yellow dice")
            break
        else:
            print("Choose again!")
    print_State(current_State)

    c = 0
    while True:

        if turn == USER_RED:
            if c > 0:
                if isFlippable(current_State, PROGRAM_WHITE)[0]:
                    human_flip(USER_RED)
                    print_State(current_State)
                else:
                    print("No valid flip available! Just place your tile!")

            humanMove_P1()
            print_State(current_State)

            turn = PROGRAM_WHITE

        elif turn == PROGRAM_WHITE:

            # move here
            m = max(current_State, 0, -MAXEVAL, MAXEVAL)

            if c > 0:  # provide the type of tile you want to flip
                if isFlippable(current_State, USER_RED)[0]:

                    print("Ace flips.....")

                    # flip
                    flipRow = m.flipRow
                    flipCol = m.flipCol
                    flipToRow = m.flipToRow
                    flipToCol = m.flipToCol

                    if current_State.cell[flipRow][flipCol] == 1:
                        current_State.cell[flipToRow][flipToCol] = 2
                        current_State.cell[flipRow][flipCol] = 0
                    elif current_State.cell[flipRow][flipCol] == 2:
                        current_State.cell[flipToRow][flipToCol] = 1
                        current_State.cell[flipRow][flipCol] = 0

                    print_State(current_State)
                else:
                    print("No valid flip available!")

            print("Ace moves.....")

            operator.row = m.row
            operator.col = m.col
            #move and color
            AIcolor = m.color
            makeMove(current_State, operator, AIcolor)
            print_State(current_State)

            turn = USER_RED

        c = c+1

        print()
        print("-------------------------------------------")
        finalResult = isTerminal(current_State)
        if finalResult:
            if finalResult == 1 or finalResult == 2:
                print("Player 1 with dice Red/Blue wins!")
            elif finalResult == 3 or finalResult == 4:
                print("Ace wins!")
            elif finalResult == 5:
                print("TIE!")

        if isTerminal(current_State):
            break


# In[114]:


# Implement humanVsAI
def humanVBob():
    # Add who wants to gofirst functionality
    print("Let's play the game Player 1 vs Bob")
    while True:
        choice = input("Who should go first? (1=User  2=Bob): ")
        if int(choice) == 1:
            turn = USER_RED
            print("You will have Red/Blue dice")
            break
        elif int(choice) == 2:
            turn = PROGRAM_WHITE
            print("Bob will have White/Yellow dice")
            break
        else:
            print("Choose again!")
    print_State(current_State)

    # Impleemnet flip in second turn
    c = 0
    while True:

        if turn == USER_RED:
            if c > 0:
                if isFlippable(current_State, PROGRAM_WHITE)[0]:
                    human_flip(turn)
                    print_State(current_State)
                else:
                    print("No valid flip available! Just place your tile!")

            humanMove_P1()
            print_State(current_State)

            turn = PROGRAM_WHITE

        elif turn == PROGRAM_WHITE:

            # move here
            m = max2(current_State, 0, -MAXEVAL, MAXEVAL)

            if c > 0:  # provide the type of tile you want to flip
                if isFlippable(current_State, USER_RED)[0]:

                    print("Bob flips.....")

                    # flip
                    flipRow = m.flipRow
                    flipCol = m.flipCol
                    flipToRow = m.flipToRow
                    flipToCol = m.flipToCol

                    if current_State.cell[flipRow][flipCol] == 1:
                        current_State.cell[flipToRow][flipToCol] = 2
                        current_State.cell[flipRow][flipCol] = 0
                    elif current_State.cell[flipRow][flipCol] == 2:
                        current_State.cell[flipToRow][flipToCol] = 1
                        current_State.cell[flipRow][flipCol] = 0

                    print_State(current_State)
                else:
                    print("No valid flip available!")

            print("Bob moves.....")

            operator.row = m.row
            operator.col = m.col
            #move and color
            AIcolor = m.color
            makeMove(current_State, operator, AIcolor)
            print_State(current_State)

            turn = USER_RED

        c = c+1

        print()
        print("-------------------------------------------")
        finalResult = isTerminal(current_State)
        if finalResult:
            if finalResult == 1 or finalResult == 2:
                print("Player 1 with dice Red/Blue wins!")
            elif finalResult == 3 or finalResult == 4:
                print("Bob wins!")
            elif finalResult == 5:
                print("TIE!")

        if isTerminal(current_State):
            break


# In[122]:


print("--------------------Welcome to the Rubik's Flip!---------------------")
print("You can play with a Random player, Player2(Human Player) and 2 AI players- Ace and Bob")
play = 1
while play != 0:
    play = int(
        input("Choose a player! (1=Random, 2=Ace, 3=Bob 4=Player2, 0 to exit): "))
    cell = [[]]
    cell = [[0 for i in range(4)] for i in range(4)]
    current_State = State()
    current_State.cell = cell
    if play == 1:
        humanVRandom()

    elif play == 2:
        humanVAI()

    elif play == 3:
        humanVBob()

    elif play == 4:
        humanVhuman()

    elif play == 0:
        break

    else:
        print("Please choose again!")


# In[ ]:


# In[ ]:
