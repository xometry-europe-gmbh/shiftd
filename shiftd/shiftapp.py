#!/usr/bin/env python3.7

import argparse
import logging
import sys

from pathlib import Path

import toml

import shiftd
from shiftd.utils import CustomHelpFormatter


ERROR_CONFIG = 1
ERROR_CONFIG_PARSING = 2

logging.basicConfig(format=shiftd.LOG_FMT, level=shiftd.LOG_LVL)
log = logging.getLogger(__name__)


def parse_config(file: str) -> shiftd.CONFIG_TYPE:
    if Path(file).exists():
        try:
            return toml.load(file)
        except IndexError:
            log.error('Unable to load TOML')
        except toml.TomlDecodeError:
            log.error('Unable to decode TOML')
        return None
    else:
        raise FileNotFoundError(file)


def parse_cmdline() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
    parser = argparse.ArgumentParser(description=f'{shiftd.SHIFTAPP_DESC} {shiftd.__version__}')

    parser.add_argument('-c', '--config', default=None,
                        help='configuration file', metavar='<config_file>')

    return parser.parse_args()


def main() -> None:
    shiftd.ARGS = parse_cmdline()

    try:
        if shiftd.ARGS.config is None:
            raise FileNotFoundError('<undef>')

        shiftd.CONFIG = parse_config(shiftd.ARGS.config)

        if not shiftd.CONFIG:
            log.error("Can't parse configuration file: %s", shiftd.ARGS.config)
            sys.exit(ERROR_CONFIG_PARSING)
    except FileNotFoundError as exc:
        log.error('Configuration file not found: %s', exc.args[0])
        log.info('Use `-c` arg to specify a correct one')
        sys.exit(ERROR_CONFIG)

    shiftd.DEBUG = shiftd.CONFIG['main']['debug']
    shiftd.RPC_URI = (f'{shiftd.CONFIG["rpc"]["proto"]}://'
                      f'{shiftd.CONFIG["rpc"]["host"]}:{shiftd.CONFIG["rpc"]["port"]}')

    if shiftd.DEBUG:
        log.info('Debug mode is ON')
        log.info('Running configuration: %s', Path(shiftd.ARGS.config).resolve())
        log.info('RPC_URI -> %r', shiftd.RPC_URI)


if __name__ == '__main__':
    main()
