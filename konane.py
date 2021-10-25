import random
import copy

branchingNum = 0
numCutoffs = 0
numCalls = 0
staticNum = 0

# Class for the Konane game board
class KonaneBoard:
    # initializes the konane board including indexing
    def __init__(self, size):
        self.positionList = []
        self.index = [i for i in range(1, size + 1)]
        cur = 0
        
        # Filling board
        for i in range(size):
            self.positionList.append([])
            for j in range(size):
                cur = 0
                cur = (i + j) %2

                if cur == 0:
                    self.positionList[i].append("B")
                else:
                    self.positionList[i].append("W")

    # moves a piece from an its initial position to an end position
    def movePiece(self, initPos, endPos):
        # store and remove piece
        pieceMoved = self.positionList[initPos[0]][initPos[1]]
        self.positionList[initPos[0]][initPos[1]] = " "

        # all peices jumped
        rangeX = sorted([initPos[0], endPos[0]+1])
        rangeY = sorted([initPos[1], endPos[1]+1])
        # removes pieces jumped
        for i in range(*rangeX):	
            for j in range(*rangeY):
                self.positionList[i][j] = " "

        self.positionList[endPos[0]][endPos[1]] = pieceMoved

    # returns the board as a string
    def __str__(self):
        boardPrint = "  "

        for num in self.index:
            boardPrint = boardPrint + str(num) + " "
        rowNum = 1
        boardPrint = boardPrint + "\n"

        for rows in self.positionList:
            boardPrint = boardPrint + str(rowNum) + " "

            for r in rows:
                boardPrint = boardPrint + r + " "
            rowNum = rowNum + 1
            boardPrint = boardPrint + "\n"

        return boardPrint

# Class that controls running the konane game
class Konane:
    # initializes the game values
    def __init__(self, board, boardSize, agent=0, prevMove = ()):
        self.endgame = False
        self.board = board
        self.boardSize = boardSize
        self.prevMove = prevMove
        self.curAgent = agent
        self.agentChar = ('B','W')

    # makes the current agent perform a random possible move
    def randomMove(self):
        if len(self.getPossibleMoves(self.curAgent)) != 0:
            randMove = random.choice(self.getPossibleMoves(self.curAgent))
            self.board.movePiece(randMove[0], randMove[1])

            print(self.board)

            self.prevMove = randMove
            self.curAgent = 1 - self.curAgent
        else:
            self.endgame = True
            print ("%s Lost" %(self.agentChar[self.curAgent]))

    # makes the current agent perform a move based on the minimax with or without alphabeta pruning
    def minimaxMove(self, isAlphaBeta):
        global numCalls

        # if there are possible moves
        if len(self.getPossibleMoves(self.curAgent)) != 0:
            # chooses the algorith being run
            if (isAlphaBeta):
                agentMove = alphabeta(self, float("-inf"), float("inf"), 0)
            else:
                agentMove = minimax(self,  0)
            agentMove = agentMove[1]

            # print(self.board)

            self.board.movePiece(agentMove[0], agentMove[1])    
            print(self.board)

            self.curAgent = 1 - self.curAgent
            self.prevMove = agentMove
        # game is over
        else:
            self.endgame = True
            print ("%s Lost" %(self.agentChar[self.curAgent]))

    # calculates and returns the static evaluation count
    def evalStatic(self):
        oppMoves = self.getPossibleMoves(1)
        moves = self.getPossibleMoves(0)

        if oppMoves == 0:
            return float("inf")
        if moves == 0:
            return float("-inf")

        evalNum = len(moves) - len(oppMoves)
        return evalNum

    # returns if a move is possible of a given agent
    def isPossible(self, curAgent, move):
        iniPos, endPos = move
        # checks end position
        if not endPos[0] in range(self.boardSize) or not endPos[1] in range(self.boardSize):
            return False 
        # checks is empty
        if self.board.positionList[endPos[0]][endPos[1]] != ' ':
            return False
        # checks if position is the current piece 
        if self.board.positionList[iniPos[0]][iniPos[1]] != self.agentChar[curAgent]:
            return False    

        jumped = (iniPos[0] - (iniPos[0] - endPos[0])/2, iniPos[1] - (iniPos[1] - endPos[1])/2)
        oppAgent = 1 - curAgent 
        # checks jumping
        if self.board.positionList[jumped[0]][jumped[1]] != self.agentChar[oppAgent]:
            return False 

        return True

    # returns a list of possible moves for a given agent
    def getPossibleMoves(self, curAgent):
        possibleMoves = []

        for row in range(self.boardSize):
            for col in range(self.boardSize):

                if self.board.positionList[row][col] == self.agentChar[curAgent]:
                    pos = (row,col)
                    moveList = [(pos, (pos[0] - 2, pos[1])), (pos, (pos[0], pos[1]+2)), (pos, (pos[0] + 2, pos[1])), (pos, (pos[0], pos[1] - 2))]

                    for i in range(len(moveList)):
                        move = moveList[i]

                        # checks if a jump can be made
                        if self.isPossible(curAgent,move):
                            possibleMoves.append(move)
                            initPos, endPos = move

                            boardCopy = copy.deepcopy(self.board)
                            boardCopy.movePiece(initPos,endPos)

                            newMoveList = [(endPos, (endPos[0]-2, endPos[1])), (endPos, (endPos[0], endPos[1] + 2)), (endPos, (endPos[0] + 2, endPos[1])), (endPos, (endPos[0], endPos[1] - 2))]
                            nextMove = newMoveList[i]
                            newGame = Konane(boardCopy, self.boardSize,curAgent)

                            # checks for additional jumps
                            while(newGame.isPossible(curAgent, nextMove)):
                                iniPos = endPos
                                endPos = nextMove[1]
                                possibleMoves.append((iniPos, endPos))

                                boardCopy = copy.deepcopy(boardCopy)
                                boardCopy.movePiece(iniPos, endPos)

                                newMoveList = [(endPos, (endPos[0]-2,endPos[1])), (endPos, (endPos[0], endPos[1] + 2)), (endPos, (endPos[0] + 2, endPos[1])), (endPos, (endPos[0],endPos[1] - 2))]
                                nextMove = newMoveList[i]
                                newGame = Konane(boardCopy,newGame.boardSize,curAgent)
        return possibleMoves

    # returns a list of successors for the current agent
    def getSucc(self):
        successors = []
        for move in self.getPossibleMoves(self.curAgent):
            copyBoard = copy.deepcopy(self.board)
            copyBoard.movePiece(move[0], move[1])
            successors.append(Konane(copyBoard, self.boardSize, 1 - self.curAgent, move))

        return successors

# runs the minimax algorithm for a given depth and returns the best move
def minimax(stateGame, depth):
    global branchingNum
    global numCutoffs
    global numCalls
    global staticNum

    # controls the depth bound
    if depth == 2:
        staticNum += 1
        return (stateGame.evalStatic(), None)
    # max function for the algorithm     
    elif stateGame.curAgent == 0:
        numCalls += 1
        bestmove = None
        score = float('-inf')

        for succState in stateGame.getSucc():
            newScore, _ = minimax(succState, depth + 1)
            branchingNum += 1

            if (newScore > score):
                score = newScore
                bestmove = succState.prevMove

        return (score, bestmove)
    # min function for the algorithm 
    else:
        bestmove = None
        numCalls += 1

        score = float('inf')

        for succState in stateGame.getSucc():
            newScore, _ = minimax(succState, depth + 1)
            branchingNum += 1
            
            if newScore < score:
                score = newScore
                bestmove = succState.prevMove

        return (score, bestmove)

# runs the minimax algorithm with alphabeta pruning for a given depth and returns the best move
def alphabeta(stateGame, alpha, beta, depth):
    global branchingNum
    global numCutoffs
    global numCalls
    global staticNum

    # controls the depth bound
    if depth == 3:
        staticNum += 1
        return (stateGame.evalStatic(), None)
    # max function for the algorithm 
    elif stateGame.curAgent == 0:
        bestmove = None
        numCalls += 1

        for succState in stateGame.getSucc():
            score, _ = alphabeta(succState, alpha, beta, depth+1)
            branchingNum += 1
            
            if alpha >= beta:
                numCutoffs += 1
                return (beta, bestmove)

            if score > alpha:
                alpha = score
                bestmove = succState.prevMove

        return (alpha, bestmove)
    # min function for the algorithm     
    else: 
        bestmove = None
        numCalls += 1

        for succState in stateGame.getSucc():
            score, _ = alphabeta(succState, alpha, beta, depth+1)
            branchingNum += 1

            if beta <= alpha:
                numCutoffs+= 1
                return (alpha, bestmove)

            if score < beta:
                beta = score
                bestmove = succState.prevMove

        return (beta, bestmove)

# runs the konane game
def runGame(stateGame):
    # players remove initial pieces
    stateGame.board.positionList[3][3] = " "
    stateGame.board.positionList[3][4] = " "
    print(stateGame.board)

    # runs the game while game has not ended 
    while stateGame.endgame != True:
        # agent 1 moves
        if stateGame.curAgent == 0:
            stateGame.randomMove()
        # agent 2 moves
        else:
            stateGame.minimaxMove(True)

# is the main function that the game is started in
if __name__ == '__main__':
    runGame(Konane(KonaneBoard(8), 8))
    staticEvalNum = branchingNum/(numCalls+0.0)
    print("Branching Factor Num: %f\nCutoff Num: %d\nStatic Evaluation Num: %d\n" % (staticEvalNum, numCutoffs, staticNum))
