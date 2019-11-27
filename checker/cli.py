# /usr/bin/python3

import argparse
import sys
import bandit

from checker.complexityChecker.complexity import flake8
from checker.pylint_checker.pylint import comm
from checker.coverage_checker.cov import Coverage


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')


PARSER = argparse.ArgumentParser()

PARSER.add_argument('-b',
                    '--basepath',
                    metavar='BASEPATH',
                    type=str,
                    help='local basepath of repo',
                    required=True)

PARSER.add_argument('-cov',
                    '--coverage',
                    type=str2bool,
                    nargs='?',
                    const=True,
                    metavar='COVERAGE',
                    help='check coverage of repo')

PARSER.add_argument('-s',
                    '--code_style',
                    type=str2bool,
                    nargs='?',
                    const=True,
                    metavar='code_style',
                    help='check code style of repo')

PARSER.add_argument('-cmp',
                    '--complexity',
                    type=str2bool,
                    nargs='?',
                    const=True,
                    metavar='complexity',
                    help='check code complexity of repo')

PARSER.add_argument('-v',
                    '--vulnerability',
                    type=str2bool,
                    nargs='?',
                    const=True,
                    metavar='vulnerability',
                    help='check vulnerability of repo')

PARSER.add_argument('-o',
                    '--output',
                    metavar='OUPTUT_DIR',
                    type=str,
                    help='output path',
                    default='')


def run_command(args):
    score = 0
    count = 0
    if args.coverage is True:
        score = score + Coverage(args.basepath).coverage_rate()
        count = count + 1
    if args.code_style is True:
        score = score + comm(args.basepath)
        count = count + 1
    if args.complexity is True:
        score = score + flake8(args.basepath)
        count = count + 1
    if args.vulnerability is True:
        # TODO score = score + returned value of vulns
        count = count + 1
    print(score / max(count, 1))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.argv.append('-h')
    args = PARSER.parse_args()
    run_command(args)
