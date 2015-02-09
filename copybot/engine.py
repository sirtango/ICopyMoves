"""CopyBot Engine"""

from copybot.gtp import intval, colorval, vertexval, point2vertex, GTPError
from copybot.board import Board
from copybot.bot import CopyBot


class Engine(object):
    """Bot engine.

    Everything that doesn't start with an underscore will
    be make it public and available as a command.
    """

    name = 'CopyBot'
    version = '0.1'

    def __init__(self):
        self._acceptable_sizes = set((9, 13, 19))
        self._board = Board(9)
        self._bots = [CopyBot(self._board)]

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
        vertex = vertexval(vertex, self._board.size)

        self._board.play(color, vertex)

    def genmove(self, color):
        color = colorval(color)
        point = None

        for bot in self._bots:
            point = bot.genmove(color)

            if point:
                break

        self._board.play(color, point)

        if point:
            vertex = point2vertex(point[0], point[1], self._board.size)
        else:
            vertex = 'pass'

        return vertex

    def showboard(self):
        return str(self._board)

