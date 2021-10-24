class GameBoard:
    def __init__(self, size):
        print("starting game")
        self.positionList = []
        self.index = [i for i in range(1, size + 1)]
        cur = 0

        for i in range(size):
            self.positionList.append([])
        
        # Filling board
        for i in range(size):
            for j in range(size):
                cur = 0
                cur = (i + j) %2

                if cur == 0:
                    self.positionList[i].append("B")
                else:
                    self.positionList[i].append("W")


    def movePiece(self, initPos, endPos):
        """ function moves pieces on board """
        pieceMoved = self.positionList[initPos[0]][initPos[1]]
        self.positionList[initPos[0]][initPos[1]] = " "

        rangeX = sorted([initPos[0], endPos[0]+1])
        rangeY = sorted([initPos[1], endPos[1]+1])
        
        for i in range(*rangeX):	
            for j in range(*rangeY):
                self.positionList[i][j] = " "

        self.positionList[endPos[0]][endPos[1]] = pieceMoved


    def __str__(self):
        """ Prints the board """
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
