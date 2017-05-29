import sys

from command import init


def handle(args):
    if args[0] == 'init':
        init.command()


if __name__ == '__main__':
    handle(sys.argv[1:])
