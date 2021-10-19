class Konane:

    def __init__(self, n):
        self.size = n
        self.reset()

    def reset(self):
        """
        Resets the starting board state.
        """
        self.board = []
        value = 'B'
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(value)
                value = self.opponent(value)
            self.board.append(row)
            if self.size%2 == 0:
                value = self.opponent(value)

    def __str__(self):
        return self.boardToStr(self.board)

    def boardToStr(self, board):
        """
        Returns a string representation of the konane board.
        """
        result = "  "
        for i in range(self.size):
            result += str(i) + " "
        result += "\n"
        for i in range(self.size):
            result += str(i) + " "
            for j in range(self.size):
                result += str(board[i][j]) + " "
            result += "\n"
        return result