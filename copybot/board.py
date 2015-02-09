
class Group(object):
    """Group inside the Board."""

    def __init__(self, board, row, col):
        self.points = set()
        self.color = board.state[row][col]
        self.is_surrounded = self.color is not None

        to_handle = set()
        to_handle.add((row, col))

        while to_handle:
            r0, c0 = to_handle.pop()
            color0 = board.state[r0][c0]

            self.points.add((r0, c0))

            for r1, c1 in [(r0-1, c0), (r0+1, c0), (r0, c0-1), (r0, c0+1)]:
                if r1 < 0 or r1 >= board.size or c1 < 0 or c1 >= board.size:
                    continue

                color1 = board.state[r1][c1]

                if not color1:
                    self.is_surrounded = False
                elif color1 == color0:
                    if (r1, c1) not in self.points:
                        to_handle.add((r1, c1))


class Board(object):
    """Go board."""

    def __init__(self, size):
        self.size = size
        self.history = []

    def clear(self):
        self.state = [[None
            for x in range(self.size)]
            for x in range(self.size)]
        self.history = []

    def play(self, color, vertex):
        self.history.append((color, vertex))

        if not vertex:
            return # pass

        row, col = vertex

        if 0 > row or 0 > col:
            raise IndexError
        if self.state[row][col] is not None:
            raise ValueError('{},{} already exists'.format(row, col))

        self.state[row][col] = color

        for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                continue
            group = Group(self, r, c)
            if group.is_surrounded and group.color != color:
                for r, c in group.points:
                    self.state[r][c] = None

    def __str__(self):
        board = ''
        for row in self.state:
            for color in row:
                if color:
                    board = board + color
                else:
                    board = board + '.'
            board = board + '\n'
        return board

