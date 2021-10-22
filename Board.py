
class Board:
        def __init__(self, size):
                self.board1 = []
                for i in range(size):	#rows
                        self.board1.append([])

		for i in range(size):		
			for j in range(size):
				if i%2 == 0:
					if j%2 == 0:
                                                self.board1[i].append("B")
					else:
                                                self.board1[i].append("W")
				else:
					if j%2 == 0:
                                                self.board1[i].append("W")
					else:
                                                self.board1[i].append("B")

	def __str__(self):

		display = "  "
		display += "\n"
		rowNumber = 1
                for row in self.board1:
			for piece in row:
				display += piece+" "
			display += "\n"
			rowNumber += 1
		return display

        def movePiece(self, firstPos, nextPos):

                curPiece = self.board1[firstPos[0]][firstPos[1]]
                self.board1[firstPos[0]][firstPos[1]] = "."

                x_range = sorted([firstPos[0], nextPos[0]+1])
                y_range = sorted([firstPos[1], nextPos[1]+1])
                for x in range(*x_range):
			for y in range(*y_range):

                                self.board1[x][y] = "."
                self.board1[nextPos[0]][nextPos[1]] = curPiece

        def removePiece(self, pos):

                self.board1[pos[0]][pos[1]] = "."
