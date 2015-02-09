"""CopyBot Engine"""

from copybot.gtp import intval, colorval, vertexval, GTPError
from copybot.board import Board


class Engine(object):
    """Bot engine.

    Everything that doesn't start with an underscore will
    be make it public and available as a command.
    """

    name = 'CopyBot'
    version = '0.1'

    def __init__(self):
        self._acceptable_sizes = set((9, ))
        self._board = Board(9)

    def boardsize(self, size):
        size = intval(size)
        if size not in self._acceptable_sizes:
            raise GTPError('unacceptable size')

        self._board.size = size
        self._board.clear()

    def clear_board(self):
        self._board.clear()

    def play(self, color, vertex):
        color = colorval(color)
        vertex = vertexval(vertex)

        if vertex and (\
            vertex[0] >= self._board.size or \
            vertex[1] >= self._board.size):
                raise GTPError('off board {},{}'.format(*vertex))

        self._board.play(color, vertex)

    def genmove(self, color):
        color = colorval(color)
        return 'pass'

    def showboard(self):
        return str(self._board)

