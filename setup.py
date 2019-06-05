#!/usr/bin/env python3.7

import sys
import types

from io import StringIO
from os import path as op
from os.path import join
from textwrap import dedent
from typing import List

from setuptools import (
    find_packages,
    setup,
)
from setuptools.command.test import test as TestCommand

import shiftd


def _read(filename: str) -> str:
    try:
        fp = open(join(op.dirname(__file__), filename))
        try:
            return fp.read()
        finally:
            fp.close()
    except (IOError, OSError):  # IOError/2.7, OSError/3.5
        return str()


def _read_requirements(filename: str) -> List[str]:
    is_valid = lambda _: _ and not any(_.startswith(ch) for ch in ['#', '-'])

    data = getattr(types, 'UnicodeType', str)(_read(filename))
    return list(_.strip() for _ in StringIO(data) if is_valid(_.strip()))  # type: ignore


class PyTest(TestCommand):
# pylint: disable=attribute-defined-outside-init
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self) -> None:
        super().initialize_options()
        self.pytest_args: List[str] = list()

    def run_tests(self) -> None:
        # Import here, cause outside the eggs aren't loaded.
        import pytest

        if isinstance(self.pytest_args, str):
            self.pytest_args = self.pytest_args.split()

        errno = pytest.main(args=self.pytest_args)
        sys.exit(errno)


setup_params = dict(
    name='ShiftD',
    version=shiftd.__version__,
    description=shiftd.SHIFTD_DESC,
    long_description=dedent("""
        The Autodesk Fusion 360 Dispatcher addin that communicates with an external apps using ZMQ/RPC server.
        """).strip(),
    author='Alex Kopchikov',
    author_email='alexk3y@gmail.com',
    url='https://shift.parts',

    classifiers=dedent("""
        Natural Language :: English
        Development Status :: 3 - Alpha
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows :: Windows 10
        Programming Language :: Python
        Programming Language :: Python :: 3.7
        """),
    license='Proprietary',
    keywords=[],

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'shiftapp = shiftd.shiftapp:main',
        ]
    },

    install_requires=_read_requirements('requirements.txt'),
    setup_requires=[
        'wheel',
    ],
    tests_require=_read_requirements('requirements-test.txt'),

    cmdclass={'test': PyTest},
)


def main() -> None:
    setup(**setup_params)


if __name__ == '__main__':
    main()
