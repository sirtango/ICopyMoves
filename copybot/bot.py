
class CopyBot(object):
    def __init__(self, board):
        self.board = board

    def genmove(self, color):
        # If this is the first move, we start with tengen.
        if len(self.board.history) == 0:
            tengen = int((self.board.size + 1) / 2) - 1
            return tengen, tengen

        last = self.board.history[-1]

        # This is an error, if the last move was from the
        # same color that has to generate a move it will
        # pass instead of raiseing an error.
        if last[0] == color:
            return None

        # If the last move is a pass, we pass too.
        if last[1] is None:
            return None

        row, col = self.invert(*last[1])

        if self.board.state[row][col] is not None:
            return None

        return row, col

    def invert(self, row, col):
        return self.board.size - 1 - row, self.board.size - 1 - col

