from random import randint
import copy
import sys

startBoard = [['.','.','.','.','.','.','.','.','.'],
              ['.','.','.','.','.','.','.','.','.'],
              ['.','.','.','.','.','.','.','.','.'],
              ['.','.','.','.','.','.','.','.','.']]


def printBoard(gameBoard):
    print("+-------+-------+")
    # game blocks 1 & 2
    printGameBlock(gameBoard, 0, 1)
    print "+-------+-------+"
    # game blocks 3 & 4
    printGameBlock(gameBoard, 2, 3)
    print("+-------+-------+")


def printGameBlock(gameBoard, blockA, blockB):
    for row in range(0, 3):
        print "|",
        # left game block
        for col in range(0, 3):
            print gameBoard[blockA][col + row * 3],
        print "|",
        # right game block
        for col in range(0, 3):
            print gameBoard[blockB][col + row * 3],
        print "|"


# A move will have the form: b/p bd , where b/p is the block and position
# describing the location in which a token is placed,
# and bd is a block and direction for rotation 
def getMove(gameBoard):
    while True:
        move = raw_input("What is your move? (b/p bd): ")
        temp = move.split(' ')
        
        if (len(temp) == 2):
            block, position = [int(x) for x in temp[0].split('/')]
            rotatedBlock = int(temp[1][0])
            direction = temp[1][1].upper()
        
            if (checkIfValidMove(gameBoard, block, position, rotatedBlock, direction)):
                return move
                break
            else: 
                print "Invalid move! Try again"
        else:
            print "Invalid move! Try again."


# check if the move that was selected is available
def checkIfValidMove(gameBoard, block, position, rotatedBlock, direction):
    validGameBlocks = [1, 2, 3, 4]
    validPositions = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if (block in validGameBlocks and rotatedBlock in validGameBlocks):
        if (position in validPositions and (direction == 'L' or direction == 'R')):
            if(gameBoard[block - 1][position - 1] == '.'):
                return True
    return False


# place the token on the empty spot on the board (do not rotate yet)
def makeMove(gameBoard, move, token):
    # initialize board to return later
    # board = [range(9) for x in range(4)]
    # print move + ' ' + token
    board = copy.deepcopy(gameBoard)
    c = token.lower()
    temp = move.split(' ')
    block, position = [int(x) for x in temp[0].split('/')]
    board[block - 1][position - 1] = c
    return board


# before rotating, check if won
def rotateBoard(gameBoard, move):

    # initialize board to return later
    # board = [range(9) for x in range(4)]
    board = copy.deepcopy(gameBoard)

    temp = move.split(' ')
    rotatedBlock = int(temp[1][0])
    direction = temp[1][1].upper()
    
    newBlock = []
    rotated = []
    oldBlock = board[rotatedBlock - 1]
    temp = [oldBlock[i:i + 3] for i in xrange(0, len(oldBlock), 3)]
    if (direction == 'R'):
        # chunk the old block list into 3 parts to rotate
        rotated = zip(*temp[::-1])
    else: 
        rotated = zip(*temp)[::-1]
    
    for c in rotated:
        for i in c:
            newBlock.append(i)
        
    board[rotatedBlock - 1] = newBlock
    return board


# check if the player won by passing in the player's token char
def checkIfWon(gameBoard, token):
    c = token.lower()
    
    # 0-initialize matrix
    matrix = [range(6) for x in range(6)]

    matrix[0][0:3] = gameBoard[0][0:3]
    matrix[0][3:6] = gameBoard[1][0:3]
    matrix[1][0:3] = gameBoard[0][3:6]
    matrix[1][3:6] = gameBoard[1][3:6]
    matrix[2][0:3] = gameBoard[0][6:9]
    matrix[2][3:6] = gameBoard[1][6:9]
    matrix[3][0:3] = gameBoard[2][0:3]
    matrix[3][3:6] = gameBoard[3][0:3]
    matrix[4][0:3] = gameBoard[2][3:6]
    matrix[4][3:6] = gameBoard[3][3:6]
    matrix[5][0:3] = gameBoard[2][6:9]
    matrix[5][3:6] = gameBoard[3][6:9]

    # checking rows
    for i in range(0, 6):
        row = matrix[i]
#         print 'Row ' + str(i) + ': ' + str(row)
        if (row[0:5] == [c, c, c, c, c] or row[1:6] == [c, c, c, c, c]):
            return True

    # checking diagonals
    if ([matrix[1][1], matrix[2][2], matrix[3][3], matrix[4][4], matrix[5][5]] == [c, c, c, c, c] or
        [matrix[0][0], matrix[1][1], matrix[2][2], matrix[3][3], matrix[4][4]] == [c, c, c, c, c] or
        [matrix[1][0], matrix[2][1], matrix[3][2], matrix[4][3], matrix[5][4]] == [c, c, c, c, c] or
        [matrix[0][1], matrix[1][2], matrix[2][3], matrix[3][4], matrix[4][5]] == [c, c, c, c, c]):
        return True
    
    # rotate the matrix to check columns
    rMatrix = zip(*matrix[::-1])
    
    # convert each tuple back into a list
    for i in range(0,6):
        rMatrix[i] = list(rMatrix[i])

    # checking rows of rotated matrix 
    for i in range(0, 6):
        row = rMatrix[i]
#         print 'Row ' + str(i) + ': ' + str(row)
        if (row[0:5] == [c, c, c, c, c] or row[1:6] == [c, c, c, c, c]):
            return True

    # checking diagonals of rotated matrix
    if ([rMatrix[1][1], rMatrix[2][2], rMatrix[3][3], rMatrix[4][4], rMatrix[5][5]] == [c, c, c, c, c] or
        [rMatrix[0][0], rMatrix[1][1], rMatrix[2][2], rMatrix[3][3], rMatrix[4][4]] == [c, c, c, c, c] or
        [rMatrix[1][0], rMatrix[2][1], rMatrix[3][2], rMatrix[4][3], rMatrix[5][4]] == [c, c, c, c, c] or
        [rMatrix[0][1], rMatrix[1][2], rMatrix[2][3], rMatrix[3][4], rMatrix[4][5]] == [c, c, c, c, c]):
        return True

    return False 


# have user choose color
# set the ai's color to the other color
def setTokenColor():
    userColor = ''
    while not (userColor == 'B' or userColor == 'W'):
        userColor = raw_input("Choose your token color (B or W): ").upper()
    
    if userColor == 'B':
        return ['B', 'W']
    else:
        return ['W', 'B']
     
        
# choose if user or ai goes first
# 0 is the user
# 1 is the computer
def chooseFirstMove(userName):
    turn = randint(0, 1)
    return userName if turn == 0 else "AI"


# returns true when every space on the board is taken
def boardIsFull(gameBoard):
    for block in gameBoard:
        for space in block:
            if (space == '.'):
                return False
    return True

def countEmptySpots(gameBoard):
    e = 0
    for block in gameBoard:
        for space in block:
            if (space == '.'):
                e += 1
    return e

def outputFile(gameBoard, firstTurn, userName, userColor, aiColor, allMoves):
    f = open("gameresults.txt", "w")
    if (firstTurn == userName):
        f.write("Player 1 Name (player who moves first): " + userName + "\n")
        f.write("Player 2 Name: AI\n")
        f.write("Player 1 Token Color: " + userColor + "\n")
        f.write("Player 2 Token Color: " + aiColor + "\n")
    else:
        f.write("Player 1 Name (player who moves first): AI\n")
        f.write("Player 2 Name: " + userName + "\n")
        f.write("Player 1 Token Color: " + aiColor + "\n")
        f.write("Player 2 Token Color: " + userColor + "\n")
        
    f.write("Moves Made:\n")
    for move in allMoves:
        f.write(move + "\n")
    
    f.write("Win Configuration:\n")
    for row in range(0, 3):
        # left game block
        for col in range(0, 3):
            f.write( gameBoard[0][col + row * 3] + ' ')
        # right game block
        for col in range(0, 3):
            f.write( gameBoard[1][col + row * 3] + ' ')
        f.write("\n")
    for row in range(0, 3):
        # left game block
        for col in range(0, 3):
            f.write( gameBoard[2][col + row * 3] + ' ')
        # right game block
        for col in range(0, 3):
            f.write( gameBoard[3][col + row * 3] + ' ')
        f.write("\n")
    
    f.close()

def alphabeta(board, maximize, token, depth, a, b):
    if gameOver(board) or depth == 0:
        return boardValue(board, token)
    
    if maximize:
        v = -sys.maxint
        for child in children(board, token):
            v = max(v, alphabeta(child, False, opponent(token), depth - 1, a, b))
            a = max(a, v)
            if b <= a:
                break
        return v
    else:
        v = sys.maxint
        for child in children(board, token):
            v = min(v, alphabeta(child, True, opponent(token), depth - 1, a, b))
            b = min(v, b)
            if b <= a:
                break
        return v

def minimax(board, maximize, token, depth):
    if gameOver(board) or depth == 0:
        return boardValue(board, token)
    
    if maximize:
        bestValue = -sys.maxint
        for child in children(board, token):
            v = minimax(child, False, opponent(token), depth - 1)
            bestValue = max(bestValue, v)
        return v
    else:
        bestValue = sys.maxint
        for child in children(board, token):
            v = minimax(child, True, opponent(token), depth - 1)
            bestValue = min(bestValue, v)
        return v

        
def boardValue(board, token):
    # value = this player's points minus other player's points
    opToken = opponent(token)
    result = (verticalPoints(board, token) - verticalPoints(board, opToken) +
           horizontalPoints(board, token)  - horizontalPoints(board, opToken))

    return result

def boardToMatrix(board):
    # initialize matrix
    matrix = [range(6) for x in range(6)]

    # copy gameboard segments to matrix
    matrix[0][0:3] = board[0][0:3]
    matrix[0][3:6] = board[1][0:3]
    matrix[1][0:3] = board[0][3:6]
    matrix[1][3:6] = board[1][3:6]
    matrix[2][0:3] = board[0][6:9]
    matrix[2][3:6] = board[1][6:9]
    matrix[3][0:3] = board[2][0:3]
    matrix[3][3:6] = board[3][0:3]
    matrix[4][0:3] = board[2][3:6]
    matrix[4][3:6] = board[3][3:6]
    matrix[5][0:3] = board[2][6:9]
    matrix[5][3:6] = board[3][6:9]
    
    return matrix

def rotateMatrix(matrix):
    # rotate the matrix into list of tuples
    rMatrix = zip(*matrix[::-1])
    
    # convert each tuple back into a list
    for i in range(0,6):
        rMatrix[i] = list(rMatrix[i])
        
    return rMatrix

def horizontalPoints(board, token):
    c = token.lower()
    matrix = boardToMatrix(board)
    points = 0
    for i in range(0,6):
        tokenCount = 0
        for j in range(0,6):
            if matrix[i][j] == c:
                tokenCount += 1
        if tokenCount == 2:
            points += 5
        elif tokenCount == 3:
            points += 50
        elif tokenCount == 4:
            points += 500
        elif tokenCount == 5:
            points += 5000
    
    return points

def verticalPoints(board, token):
    c = token.lower()
    matrix = rotateMatrix(boardToMatrix(board))
    points = 0
    for i in range(0,6):
        tokenCount = 0
        for j in range(0,6):
            if matrix[i][j] == c:
                tokenCount += 1
        if tokenCount == 2:
            points += 5
        elif tokenCount == 3:
            points += 50
        elif tokenCount == 4:
            points += 500
        elif tokenCount == 5:
            points += 5000
    
    return points
           
def gameOver(board):

    emptyFound = False
    for i in range(0,4):
        for j in range(0,9):
            if board[i][j] == '.':
                emptyFound = True
                break
    
    if ((not emptyFound) or checkIfWon(board, 'w') or checkIfWon(board, 'b')):
        # print "got to True in gameOver"
        return True
    else:
        return False

# returns a list of boards that are results of all possible moves from passed board
def children(board, token):
    # right now children will be result of place+rotate
    # can add code to have "halfway children" that result in a gameOver if you just place
    children = []
    moves = possibleMoves(board, token)
    for move in moves:
        child = makeMove(board, move, token)
        child = rotateBoard(child, move)
        children.append(child)
    
    return children

# returns list of moves in the same order as children as their results
def possibleMoves(board, token):
    # right now children will be result of place+rotate
    # can add code to have "halfway children" that result in a gameOver if you just place
    moves = []
    placements = []
    for i in range(0, 4):
        for j in range(0, 9):
            if board[i][j].lower() == '.':
                placements.append((i + 1, j + 1)) # block, cell that is vacant
                
    for placement in placements:
        for block in range(0, 4):
            # in children we store boards as results of makeMove and rotateBoard using the 
            # string move in format "b/p bd" like "3/8 2R"
            move = str(placement[0]) + "/" + str(placement[1]) + " " + str(block + 1) + "R"
            moves.append(move)

            move = str(placement[0]) + "/" + str(placement[1]) + " " + str(block + 1) + "L"
            moves.append(move)

    return moves

# accepts current board and the AI's token
def pickMove(board, token):
    results = children(board, token)
    moves = possibleMoves(board, token)
    bestValueIndex = 0
    bestValue = -sys.maxint
    for i in range(0, len(results)):
        # depth is actually 1+ what is passed to minimax or alphabeta (because we create children above)
        # value = minimax(results[i], True, token, 1)
        value = alphabeta(results[i], True, token, 1, -sys.maxint, sys.maxint)
        if (value > bestValue):
            bestValueIndex = i
            bestValue = value
        
    return moves[bestValueIndex]

def opponent(token):
    if token.lower() == 'b':
        return 'w'
    else:
        return 'b'

if __name__ == "__main__":
    print "Welcome to Pentago!"
    print ""
    
    gameIsPlaying = True
    userName = raw_input("Enter your name: ")
    userColor, aiColor = setTokenColor()
    firstTurn = chooseFirstMove(userName)
    turn = firstTurn
    allMoves = []
    
    print "Randomly selecting who will go first... " + turn + " will go first."
    
    while gameIsPlaying:
        if (turn == userName): # user makes their move
            print ""
            print "It is your turn."
            move = getMove(startBoard)
            allMoves.append(move)
            startBoard = makeMove(startBoard, move, userColor)
            
            # check if won before rotate
            if (checkIfWon(startBoard, userColor)):
                printBoard(startBoard)
                print "You Won!"
                gameIsPlaying = False
            else:
                # rotate board only if didn't already win
                startBoard = rotateBoard(startBoard, move)
                
                printBoard(startBoard)
                
                # check if both won
                if (checkIfWon(startBoard, userColor) and (checkIfWon(startBoard, aiColor))):
                    print "Tie!"
                    gameIsPlaying = False
                    
                # check if user won
                elif (checkIfWon(startBoard, userColor) and not(checkIfWon(startBoard, aiColor))):
                    print "You Won!"
                    gameIsPlaying = False
                    
                # check if computer won
                elif (not(checkIfWon(startBoard, userColor)) and checkIfWon(startBoard, aiColor)):
                    print "The rotation made the computer win! :("
                    gameIsPlaying = False
                    
                #check if board is full
                elif (boardIsFull(startBoard)):
                    print ""
                    print "No more moves can be made."
                    print "Game Over."
                    gameIsPlaying = False
                    
                # switch turns
                else:
                    turn = "AI"
            
                        
        else: # computer moves
            print ""
            print "It is the computer's turn."  
            move = pickMove(startBoard, aiColor)
            allMoves.append(move)
            startBoard = makeMove(startBoard, move, aiColor)
            
            # check if won before rotate
            if (checkIfWon(startBoard, aiColor)):
                printBoard(startBoard)
                print "You Lost!"
                gameIsPlaying = False
            else:
                # rotate board only if didn't already win
                startBoard = rotateBoard(startBoard, move)
                
                printBoard(startBoard)
                
                # check if both won after rotate
                if (checkIfWon(startBoard, aiColor) and checkIfWon(startBoard, userColor)):
                    print "Tie!"
                    gameIsPlaying = False
                # check if computer won
                elif (checkIfWon(startBoard, aiColor) and not(checkIfWon(startBoard, userColor))):
                    print "You Lost!"
                    gameIsPlaying = False
                # check if user won
                elif (not(checkIfWon(startBoard, aiColor)) and checkIfWon(startBoard, userColor)):
                    print "The rotation made you win! :)"
                    gameIsPlaying = False
                    
                # check if the board is full
                elif (boardIsFull(startBoard)):
                    print ""
                    print "No more moves can be made."
                    print "Game Over."
                    gameIsPlaying = False
                    
                # switch turns
                else:
                    turn = userName
                    
    print "Check gameresults.txt to see the game summary."
    outputFile(startBoard, firstTurn, userName, userColor, aiColor, allMoves)