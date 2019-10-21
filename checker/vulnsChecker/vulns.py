import fnmatch
import logging
import os
import sys
import textwrap

import bandit
from bandit.core import config as b_config
from bandit.core import constants
from bandit.core import manager as b_manager
from bandit.core import utils

BASE_CONFIG = 'bandit.yaml'
LOG = logging.getLogger()


def _init_logger(log_level=logging.INFO, log_format=None):
    '''Initialize the logger

    :param debug: Whether to enable debug mode
    :return: An instantiated logging instance
    '''
    LOG.handlers = []

    if not log_format:
        # default log format
        log_format_string = constants.log_format_string
    else:
        log_format_string = log_format

    logging.captureWarnings(True)

    LOG.setLevel(log_level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(log_format_string))
    LOG.addHandler(handler)
    LOG.debug("logging initialized")


def _get_options_from_ini(ini_path, target):
    """Return a dictionary of config options or None if we can't load any."""
    ini_file = None

    if ini_path:
        ini_file = ini_path
    else:
        bandit_files = []

        for t in target:
            for root, _, filenames in os.walk(t):
                for filename in fnmatch.filter(filenames, '.bandit'):
                    bandit_files.append(os.path.join(root, filename))

        if len(bandit_files) > 1:
            LOG.error('Multiple .bandit files found - scan separately or '
                      'choose one with --ini\n\t%s', ', '.join(bandit_files))
            sys.exit(2)

        elif len(bandit_files) == 1:
            ini_file = bandit_files[0]
            LOG.info('Found project level .bandit file: %s', bandit_files[0])

    if ini_file:
        return utils.parse_ini_file(ini_file)
    else:
        return None


def _init_extensions():
    from bandit.core import extension_loader as ext_loader
    return ext_loader.MANAGER


def _log_option_source(arg_val, ini_val, option_name):
    """It's useful to show the source of each option."""
    if arg_val:
        LOG.info("Using command line arg for %s", option_name)
        return arg_val
    elif ini_val:
        LOG.info("Using ini file for %s", option_name)
        return ini_val
    else:
        return None


def _running_under_virtualenv():
    if hasattr(sys, 'real_prefix'):
        return True
    elif sys.prefix != getattr(sys, 'base_prefix', sys.prefix):
        return True


def _get_profile(config, profile_name, config_path):
    profile = {}
    if profile_name:
        profiles = config.get_option('profiles') or {}
        profile = profiles.get(profile_name)
        if profile is None:
            raise utils.ProfileNotFound(config_path, profile_name)
        LOG.debug("read in legacy profile '%s': %s", profile_name, profile)
    else:
        profile['include'] = set(config.get_option('tests') or [])
        profile['exclude'] = set(config.get_option('skips') or [])
    return profile


def _log_info(args, profile):
    inc = ",".join([t for t in profile['include']]) or "None"
    exc = ",".join([t for t in profile['exclude']]) or "None"
    LOG.info("profile include tests: %s", inc)
    LOG.info("profile exclude tests: %s", exc)
    LOG.info("cli include tests: %s", args.tests)
    LOG.info("cli exclude tests: %s", args.skips)



def main(args):
    debug = (logging.DEBUG if '-d' in sys.argv or '--debug' in sys.argv else
            logging.INFO)
    _init_logger(debug)
    extension_mgr = _init_extensions()

    if args.output_format != 'custom' and args.msg_template is not None:
        parser.error("--msg-template can only be used with --format=custom")

    try:
        b_conf = b_config.BanditConfig(config_file=args.config_file)
    except utils.ConfigError as e:
        LOG.error(e)
        sys.exit(2)

    # Handle .bandit files in projects to pass cmdline args from file
    ini_options = _get_options_from_ini(args.ini_path, args.targets)
    if ini_options:
        # prefer command line, then ini file
        args.excluded_paths = _log_option_source(
            args.excluded_paths,
            ini_options.get('exclude'),
            'excluded paths')

        args.skips = _log_option_source(
            args.skips,
            ini_options.get('skips'),
            'skipped tests')

        args.tests = _log_option_source(
            args.tests,
            ini_options.get('tests'),
            'selected tests')

        ini_targets = ini_options.get('targets')
        if ini_targets:
            ini_targets = ini_targets.split(',')

        args.targets = _log_option_source(
            args.targets,
            ini_targets,
            'selected targets')

        # TODO(tmcpeak): any other useful options to pass from .bandit?

        args.recursive = _log_option_source(
            args.recursive,
            ini_options.get('recursive'),
            'recursive scan')

        args.agg_type = _log_option_source(
            args.agg_type,
            ini_options.get('aggregate'),
            'aggregate output type')

        args.context_lines = _log_option_source(
            args.context_lines,
            ini_options.get('number'),
            'max code lines output for issue')

        args.profile = _log_option_source(
            args.profile,
            ini_options.get('profile'),
            'profile')

        args.severity = _log_option_source(
            args.severity,
            ini_options.get('level'),
            'severity level')

        args.confidence = _log_option_source(
            args.confidence,
            ini_options.get('confidence'),
            'confidence level')

        args.output_format = _log_option_source(
            args.output_format,
            ini_options.get('format'),
            'output format')

        args.msg_template = _log_option_source(
            args.msg_template,
            ini_options.get('msg-template'),
            'output message template')

        args.output_file = _log_option_source(
            args.output_file,
            ini_options.get('output'),
            'output file')

        args.verbose = _log_option_source(
            args.verbose,
            ini_options.get('verbose'),
            'output extra information')

        args.debug = _log_option_source(
            args.debug,
            ini_options.get('debug'),
            'debug mode')

        args.quiet = _log_option_source(
            args.quiet,
            ini_options.get('quiet'),
            'silent mode')

        args.ignore_nosec = _log_option_source(
            args.ignore_nosec,
            ini_options.get('ignore-nosec'),
            'do not skip lines with # nosec')

        args.baseline = _log_option_source(
            args.baseline,
            ini_options.get('baseline'),
            'path of a baseline report')

    if not args.targets:
        LOG.error("No targets found in CLI or ini files, exiting.")
        sys.exit(2)
    # if the log format string was set in the options, reinitialize
    if b_conf.get_option('log_format'):
        log_format = b_conf.get_option('log_format')
        _init_logger(log_level=logging.DEBUG, log_format=log_format)

    if args.quiet:
        _init_logger(log_level=logging.WARN)

    try:
        profile = _get_profile(b_conf, args.profile, args.config_file)
        _log_info(args, profile)

        profile['include'].update(args.tests.split(',') if args.tests else [])
        profile['exclude'].update(args.skips.split(',') if args.skips else [])
        extension_mgr.validate_profile(profile)

    except (utils.ProfileNotFound, ValueError) as e:
        LOG.error(e)
        sys.exit(2)

    b_mgr = b_manager.BanditManager(b_conf, args.agg_type, args.debug,
                                    profile=profile, verbose=args.verbose,
                                    quiet=args.quiet,
                                    ignore_nosec=args.ignore_nosec)

    if args.baseline is not None:
        try:
            with open(args.baseline) as bl:
                data = bl.read()
                b_mgr.populate_baseline(data)
        except IOError:
            LOG.warning("Could not open baseline report: %s", args.baseline)
            sys.exit(2)

        if args.output_format not in baseline_formatters:
            LOG.warning('Baseline must be used with one of the following '
                        'formats: ' + str(baseline_formatters))
            sys.exit(2)

    if args.output_format != "json":
        if args.config_file:
            LOG.info("using config: %s", args.config_file)

        LOG.info("running on Python %d.%d.%d", sys.version_info.major,
                 sys.version_info.minor, sys.version_info.micro)

    # initiate file discovery step within Bandit Manager
    b_mgr.discover_files(args.targets, args.recursive, args.excluded_paths)

    if not b_mgr.b_ts.tests:
        LOG.error('No tests would be run, please check the profile.')
        sys.exit(2)

    # initiate execution of tests within Bandit Manager
    b_mgr.run_tests()
    LOG.debug(b_mgr.b_ma)
    LOG.debug(b_mgr.metrics)

    # trigger output of results by Bandit Manager
    sev_level = constants.RANKING[args.severity - 1]
    conf_level = constants.RANKING[args.confidence - 1]
    b_mgr.output_results(args.context_lines,
                         sev_level,
                         conf_level,
                         args.output_file,
                         args.output_format,
                         args.msg_template)

    if (b_mgr.results_count(sev_filter=sev_level, conf_filter=conf_level) > 0
            and not args.exit_zero):
        sys.exit(1)
    else:
        sys.exit(0)