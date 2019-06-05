#!/usr/bin/env python3.7

import pytest

from shiftd import *
from shiftd.tests.test_shiftd import *


class TestShiftd:

    def _setup(self) -> None:
        pass

    def _teardown(self) -> None:
        pass

    def test_shiftd(self) -> None:
        self._setup()
        assert True
        self._teardown()


if __name__ == '__main__':
    pytest.main(args=[__file__])
