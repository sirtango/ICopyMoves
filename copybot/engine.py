"""CopyBot Engine"""

from copybot.gtp import intval, colorval, vertexval
from copybot.gtp import GTPError


class Board(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, size):
        self.size = size
        self.clear()

    def clear(self):
        self.state = [[self.EMPTY
            for x in range(self.size)]
            for x in range(self.size)]


class State(object):
    def __init__(self):
        self._size = 9
        self._board = None

    @property
    def size(self):
        return self._size

    @size.setter
    def set_size(self, size):
        self._size = size
        if self._board:
            self._board.size = size
            self._board.clear()

    @property
    def board(self):
        if not self._board:
            self._board = Board(self.size)
        return self._board

class Engine(object):
    """Bot engine.

    Everything that doesn't start with an underscore will
    be make it public and available as a command.
    """

    name = 'CopyBot'
    version = '0.1'

    def __init__(self):
        self._acceptable_sizes = set((9, ))
        self._state = State()

    def boardsize(self, size):
        size = intval(size)
        if size not in self._acceptable_sizes:
            raise GTPError('unacceptable size')
        self._state.size = size

    def clear_board(self):
        self._state.board.clear()

    def play(self, color, vertex):
        color = colorval(color)
        vertex = vertexval(vertex)

        if vertex[0] >= self._state.size \
        or vertex[1] >= self._state.size:
            raise GTPError('off board')

        # TODO
        #print(color, vertex)

