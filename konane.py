from gameBoard import GameBoard
import copy
import random

branchingNum = 0
numCutoffs = 0
numCalls = 0
staticNum = 0


def minimax(stateGame, depth):
    global branchingNum
    global numCutoffs
    global numCalls
    global staticNum

    if depth == 3:
        staticNum += 1
        return (stateGame.evalStatic(), None)
        
    elif stateGame.curAgent == 0:
        numCalls += 1
        bestmove = None
        score = float('-inf')

        for succState in stateGame.getSucc():
            newScore, _ = minimax(succState, depth+1)
            branchingNum += 1

            if (newScore > score):
                score = newScore
                bestmove = succState.prevMove

        return (score, bestmove)

    else: 	# min function
        bestmove = None
        numCalls += 1

        score = float('inf')

        for succState in stateGame.getSucc():
            newScore, _ = minimax(succState, depth+1)
            branchingNum += 1
            
            if newScore < score:
                score = newScore
                bestmove = succState.prevMove

        return (score, bestmove)

def alphabeta(stateGame, alpha, beta, depth):
    global branchingNum
    global numCutoffs
    global numCalls
    global staticNum


    if depth == 3:
        staticNum += 1
        return (stateGame.evalStatic(), None)
        
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

class Konane:
    def __init__(self, board, boardSize, agent=0, prevMove = (( ), ( ))):
        self.endgame = 0
        self.board = board
        self.boardSize = boardSize
        self.prevMove = prevMove
        self.curAgent = agent
        self.agentChar = ('B','W')

    def randomMove(self):
        if len(self.getPossibleMoves(self.curAgent)) != 0:
            randMove = random.choice(self.getPossibleMoves(self.curAgent))
            self.board.movePiece(randMove[0], randMove[1])

            print(self.board)

            self.prevMove = randMove
            self.curAgent = 1 - self.curAgent
        else:
            self.endgame = 1
            print ("%s Lost" %(self.agentChar[self.curAgent]))

    def minimaxMove(self, isAlphaBeta):
        global numCalls

        if len(self.getPossibleMoves(self.curAgent)) != 0:
            if (isAlphaBeta):
                agentMove = alphabeta(self, float("-inf"), float("inf"), 0)
            else:
                agentMove = minimax(self,  0)
            agentMove = agentMove[1]

            print(self.board)

            if not agentMove is None:
                self.board.movePiece(agentMove[0], agentMove[1])
                
                print(self.board)

                self.curAgent = 1 - self.curAgent
                self.prevMove = agentMove

            else:
                randMove = random.choice(self.getPossibleMoves(self.curAgent))
                self.board.movePiece(randMove[0], randMove[1])

                print(self.board)

                self.curAgent = 1 - self.curAgent
                self.prevMove = agentMove
        else:
            self.endgame = 1
            print ("%s Lost" %(self.agentChar[self.curAgent]))

    def evalStatic(self):
        oppMoves = self.getPossibleMoves(1)
        moves = self.getPossibleMoves(0)

        if oppMoves == 0:
            return float("inf")
        if moves == 0:
            return float("-inf")

        evalNum = len(moves) - len(oppMoves)
        return evalNum

    def isPossible(self, curAgent, move):
        iniPos = move[0]
        endPos = move[1]

        if not endPos[0] in range(self.boardSize) or not endPos[1] in range(self.boardSize):
            return False 

        if self.board.positionList[endPos[0]][endPos[1]] != ' ':
            return False

        if self.board.positionList[iniPos[0]][iniPos[1]] != self.agentChar[curAgent]:
            return False    

        jumped = (iniPos[0] - (iniPos[0] - endPos[0])/2, iniPos[1] - (iniPos[1] - endPos[1])/2)
        oppAgent = 1 - curAgent 

        if self.board.positionList[jumped[0]][jumped[1]] != self.agentChar[oppAgent]:
            return False 

        return True

    def getPossibleMoves(self, curAgent):
        possibleMoves = []

        for row in range(self.boardSize):
            for col in range(self.boardSize):

                if self.board.positionList[row][col] == self.agentChar[curAgent]:
                    pos = (row,col)
                    moveList = [(pos, (pos[0]-2,pos[1])), (pos, (pos[0],pos[1]+2)), (pos, (pos[0]+2,pos[1])), (pos, (pos[0],pos[1]-2))]

                    for i in range(len(moveList)):
                        move = moveList[i]

                        if self.isPossible(curAgent,move):
                            possibleMoves.append(move)
                            initPos = move[0]
                            endPos = move[1]

                            boardCopy = copy.deepcopy(self.board)
                            boardCopy.movePiece(initPos,endPos)

                            newMoveList = [(endPos, (endPos[0]-2, endPos[1])), (endPos, (endPos[0], endPos[1]+2)), (endPos, (endPos[0]+2, endPos[1])), (endPos, (endPos[0], endPos[1]-2))]
                            nextMove = newMoveList[i]
                            newGame = Konane(boardCopy, self.boardSize,curAgent)

                            while(newGame.isPossible(curAgent, nextMove)):
                                iniPos = endPos
                                endPos = nextMove[1]
                                possibleMoves.append((iniPos, endPos))

                                boardCopy = copy.deepcopy(boardCopy)
                                boardCopy.movePiece(iniPos, endPos)

                                newMoveList = [(endPos, (endPos[0]-2,endPos[1])), (endPos, (endPos[0],endPos[1]+2)), (endPos, (endPos[0]+2,endPos[1])), (endPos, (endPos[0],endPos[1]-2))]
                                nextMove = newMoveList[i]
                                newGame = Konane(boardCopy,newGame.boardSize,curAgent)
        return possibleMoves

    def getSucc(self):
        successors = []

        for move in self.getPossibleMoves(self.curAgent):
            copyBoard = copy.deepcopy(self.board)
            copyBoard.movePiece(move[0], move[1])
            successors.append(Konane(copyBoard, self.boardSize, 1 - self.curAgent, move))

        return successors

def runGame(stateGame):
    stateGame.board.positionList[3][3] = " "
    print(stateGame.board)

    stateGame.board.positionList[3][4] = " "
    
    print(stateGame.board)

    while stateGame.endgame != 1:

        if stateGame.curAgent == 0:
            stateGame.randomMove()
        else:
            stateGame.minimaxMove(True)


if __name__ == '__main__':
    runGame(Konane(GameBoard(8), 8))

    print("Branching Factor Num: %f" % (branchingNum/(numCalls+0.0)))
    print("Cutoff Num: %d" % (numCutoffs))
    print("Static Evaluation Num: %d" % staticNum)
