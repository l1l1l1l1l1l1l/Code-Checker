# /usr/bin/python3

import argparse
import functools
import sys

from checker.repo_checker.repo import GitRepo

from checker.vulnsChecker.vulns import _init_extensions
import bandit
from checker.vulnsChecker.vulns import vulnsCheck

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

extension_mgr = _init_extensions()

baseline_formatters = [f.name for f in filter(lambda x:
                                                hasattr(x.plugin,
                                                        '_accepts_baseline'),
                                                extension_mgr.formatters)]
VULNS = SUBPARSERS.add_parser('vulns',
        help='find vulnerabilities in repo',
        formatter_class=argparse.RawDescriptionHelpFormatter
)
VULNS.add_argument(
    'targets', metavar='targets', type=str, nargs='*',
    help='source file(s) or directory(s) to be tested'
)
VULNS.add_argument(
    '-r', '--recursive', dest='recursive',
    action='store_true', help='find and process files in subdirectories'
)
VULNS.add_argument(
    '-a', '--aggregate', dest='agg_type',
    action='store', default='file', type=str,
    choices=['file', 'vuln'],
    help='aggregate output by vulnerability (default) or by filename'
)
VULNS.add_argument(
    '-n', '--number', dest='context_lines',
    action='store', default=3, type=int,
    help='maximum number of code lines to output for each issue'
)
VULNS.add_argument(
    '-c', '--configfile', dest='config_file',
    action='store', default=None, type=str,
    help='optional config file to use for selecting plugins and '
            'overriding defaults'
)
VULNS.add_argument(
    '-p', '--profile', dest='profile',
    action='store', default=None, type=str,
    help='profile to use (defaults to executing all tests)'
)
VULNS.add_argument(
    '-t', '--tests', dest='tests',
    action='store', default=None, type=str,
    help='comma-separated list of test IDs to run'
)
VULNS.add_argument(
    '-s', '--skip', dest='skips',
    action='store', default=None, type=str,
    help='comma-separated list of test IDs to skip'
)
VULNS.add_argument(
    '-l', '--level', dest='severity', action='count',
    default=1, help='report only issues of a given severity level or '
                    'higher (-l for LOW, -ll for MEDIUM, -lll for HIGH)'
)
VULNS.add_argument(
    '-i', '--confidence', dest='confidence', action='count',
    default=1, help='report only issues of a given confidence level or '
                    'higher (-i for LOW, -ii for MEDIUM, -iii for HIGH)'
)
output_format = 'screen' if sys.stdout.isatty() else 'txt'
VULNS.add_argument(
    '-f', '--format', dest='output_format', action='store',
    default=output_format, help='specify output format',
    choices=sorted(extension_mgr.formatter_names)
)
VULNS.add_argument(
    '--msg-template', action='store',
    default=None, help='specify output message template'
                        ' (only usable with --format custom),'
                        ' see CUSTOM FORMAT section'
                        ' for list of available values',
)
VULNS.add_argument(
    '-o', '--output', dest='output_file', action='store', nargs='?',
    type=argparse.FileType('w'), default=sys.stdout,
    help='write report to filename'
)
group = VULNS.add_mutually_exclusive_group(required=False)
group.add_argument(
    '-v', '--verbose', dest='verbose', action='store_true',
    help='output extra information like excluded and included files'
)
group.add_argument(
    '-d', '--debug', dest='debug', action='store_true',
    help='turn on debug mode'
)
group.add_argument(
    '-q', '--quiet', '--silent', dest='quiet', action='store_true',
    help='only show output in the case of an error'
)
VULNS.add_argument(
    '--ignore-nosec', dest='ignore_nosec', action='store_true',
    help='do not skip lines with # nosec comments'
)
VULNS.add_argument(
    '-x', '--exclude', dest='excluded_paths', action='store',
    default='', help='comma-separated list of paths (glob patterns '
                        'supported) to exclude from scan '
                        '(note that these are in addition to the excluded '
                        'paths provided in the config file)'
)
VULNS.add_argument(
    '-b', '--baseline', dest='baseline', action='store',
    default=None, help='path of a baseline report to compare against '
                        '(only JSON-formatted files are accepted)'
)
VULNS.add_argument(
    '--ini', dest='ini_path', action='store', default=None,
    help='path to a .bandit file that supplies command line arguments'
)
VULNS.add_argument('--exit-zero', action='store_true', dest='exit_zero',
                    default=False, help='exit with 0, '
                                        'even with results found')
python_ver = sys.version.replace('\n', '')
VULNS.add_argument(
    '--version', action='version',
    version='%(prog)s {version}\n  python version = {python}'.format(
        version=bandit.__version__, python=python_ver)
)

VULNS.set_defaults(debug=False)
VULNS.set_defaults(verbose=False)
VULNS.set_defaults(quiet=False)
VULNS.set_defaults(ignore_nosec=False)


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


@command('vulns')
def sub_command_vulns(args):
    vulnsCheck(args)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.argv.append('-h')
    args = PARSER.parse_args()
    _COMMAND2HANDLER[args.subparser_name](args)
