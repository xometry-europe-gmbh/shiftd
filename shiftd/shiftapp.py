#!/usr/bin/env python3.7

import argparse

import shiftd
from shiftd.utils import CustomHelpFormatter


def parse_cmdline() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
    parser = argparse.ArgumentParser(description=f'{shiftd.SHIFTAPP_DESC} {shiftd.__version__}')

    parser.add_argument('-c', '--config', default=None,
                        help='configuration file', metavar='<config_file>')

    return parser.parse_args()


def main() -> None:
    shiftd.ARGS = parse_cmdline()
    print(f'DEBUG: {shiftd.ARGS}')


if __name__ == '__main__':
    main()
