# /usr/bin/python3

import argparse
import functools
import sys

_COMMAND2HANDLER = {}

PARSER = argparse.ArgumentParser()
SUBPARSERS = PARSER.add_subparsers(help='sub-command help',
                                   dest='subparser_name')

REPO = SUBPARSERS.add_parser('repo', help='repo status check')
REPO_PARSERS = REPO.add_subparsers(help='sub-repo-command help',
                                     dest='repo-subparser_name')

COMMIT = REPO_PARSERS.add_parser('commit', help='get commit number by date')
COMMIT.add_argument('-b',
                    '--basepath',
                    metavar='BASEPATH',
                    type=str,
                    help='local basepath of repo',
                    required=True)


def command(name):
    def wrapper(func):
        @functools.wraps(func)
        def handler_wrap(*args, **kwargs):
            return func(*args, **kwargs)

        _COMMAND2HANDLER[name] = handler_wrap

        return handler_wrap

    return wrapper


@command('repo')
@command('commit')
def sub_command_repo_commit(args):
    print(args)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.argv.append('-h')
    args = PARSER.parse_args()
    _COMMAND2HANDLER[args.subparser_name](args)
