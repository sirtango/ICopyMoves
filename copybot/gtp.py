"""Go Text Protocol implementation"""


class GTPError(Exception):
    pass


class GTPQuit(Exception):
    pass


def intval(val):
    """Converts to internet of raise GTP error."""
    try:
        ret = int(val, 10)
    except ValueError:
        raise GTPError('invalid int: {!r}'.format(val))
    return ret


def colorval(val):
    """Convert to b/w or raise GTP error."""
    val = val.lower()
    if val == 'b' or val == 'black':
        return 'b'
    if val == 'w' or val == 'white':
        return 'w'
    raise GTPError('invalid color: {!r}'.format(val))


def vertexval(val, size):
    """Converto to row,col or raise GTP error."""
    val = val.lower()

    if val == 'pass':
        return None

    letter = str(val[0])
    number = int(val[1:], 10)

    if not 'a' <= letter <= 'z':
        raise GTPError('invalid vertex letter: {!r}'.format(val))

    if number < 1:
        raise GTPError('invalid vertex number: {!r}'.format(val))

    row = size - number
    col = ord(letter) - (ord('a') if letter < 'i' else ord('b'))

    if 0 > row or row >= size or 0 > col or col >= size:
        raise GTPError('off board')

    return row, col


def point2vertex(row, col, size):
    row = row * -1 + size
    col = col + ord('a')

    if col >= ord('i'):
        col = chr(col + 1)
    else:
        col = chr(col)

    return '{}{}'.format(col, row)


class Connection(object):
    """Connection to a GTP captable controller."""

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def write(self, line):
        self.outfile.write('{}\n\n'.format(line))
        self.outfile.flush()

    def write_success(self, id, response):
        if id:
            if response:
                self.write('={} {}'.format(id, response))
            else:
                self.write('={}'.format(id))
        else:
            if response:
                self.write('= {}'.format(response))
            else:
                self.write('=')

    def write_failure(self, id, response):
        if id:
            self.write('?{} {}'.format(id, response))
        else:
            self.write('? {}'.format(response))

    def read(self):
        for line in self.readline():
            yield self.parse(line)

    def readline(self):
        while True:
            line = self.infile.readline()
            if not line:
                break
            line = line.strip()
            line = line.partition("#")[0]
            line.replace('\t', ' ')
            if line:
                yield line

    def parse(self, line):
        words = line.split()
        if words[0].isdigit():
            id = words[0]
            cmd = words[1]
            args = words[2:]
        else:
            id = None
            cmd = words[0]
            args = words[1:]
        return id, cmd, args


class Proxy(object):
    """Proxy that adds required commands.

    It will get available commands from the given object
    members and add its own.
    """

    def __init__(self, obj):
        self.obj = obj
        self.commands = [
                'protocol_version',
                'know_command',
                'list_commands',
                'quit']

        members = dir(obj)
        for member in members:
            if not member.startswith('_'):
                self.commands.append(member)

    def __getattr__(self, name):
        if name in self.commands:
            if hasattr(self.obj, name):
                return getattr(self.obj, name)
            if hasattr(self, name):
                return getattr(self, name)
        raise GTPError('unknown command')

    def protocol_version(self):
        return '2'

    def known_command(self, command):
        return 'true' if command in self.commands else 'false'

    def list_commands(self):
        return '\n'.join(self.commands)

    def quit(self):
        raise GTPQuit


def run(connection, obj):
    proxy = Proxy(obj)

    for id, cmd, args in connection.read():
        try:
            member = getattr(proxy, cmd)
            if callable(member):
                ret = member(*args)
            else:
                ret = member
        except GTPQuit:
            break
        except GTPError as e:
            connection.write_failure(id, str(e))
        else:
            if ret:
                connection.write_success(id, str(ret))
            else:
                connection.write_success(id, None)

