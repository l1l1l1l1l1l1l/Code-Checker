# /usr/bin/python3

import argparse
import functools
import sys
import bandit

from checker.repo_checker.repo import GitRepo

from checker.vulns_checker.vulns import Check

_COMMAND2HANDLER = {}



PARSER = argparse.ArgumentParser()
SUBPARSERS = PARSER.add_subparsers(help='sub-command help',
                                   dest='subparser_name')

COMMIT = SUBPARSERS.add_parser('commit', help='get commit information of repo by date')
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


@command('commit')
def sub_command_repo_commit(args):
    GitRepo(args.basepath).print_commit_info()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.argv.append('-h')
    args = PARSER.parse_args()
    _COMMAND2HANDLER[args.subparser_name](args)
