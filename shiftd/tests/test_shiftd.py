#!/usr/bin/env python3.7

import pytest


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
