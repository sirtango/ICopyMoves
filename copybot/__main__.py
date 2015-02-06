
import sys

from copybot.gtp import Connection, run
from copybot.engine import Engine


def main():
    conn = Connection(sys.stdin, sys.stdout)
    run(conn, Engine())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

