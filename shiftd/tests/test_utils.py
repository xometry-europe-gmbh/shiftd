#!/usr/bin/env python3.7

from typing import (
    Iterable,
)

import pytest

from shiftd.utils import make_singleton


class TestUtils:
# pylint: disable=blacklisted-name
# pylint: disable=attribute-defined-outside-init
#
    def _setup(self) -> None:

        class Foo(dict):

            FOO = 33

            def foo(self) -> None:
                self.update({'foo': self.FOO})

            def bar(self, nums: Iterable[int]) -> None:
                self.update({'bar': sum(nums)})

        @make_singleton
        class Bar(Foo):

            def __init__(self, *args: int, **kwargs: str) -> None:
                self.__qux = kwargs.pop('qux', 'QUX')
                super().__init__(**kwargs)
                self.foo()
                self.bar(args)

            @property
            def qux(self) -> str:
                return self.__qux

        self.Bar = Bar

    def _teardown(self) -> None:
        del self.Bar

    def test_make_singleton(self) -> None:
        self._setup()

        args = [1, 17, 29]
        kwords = {'word': 'Apple', 'Name': 'Chloe', 'qux': 'LUX'}

        x = self.Bar(*args, **kwords)
        y = self.Bar._new()  # type: ignore # pylint: disable=no-member
        z = self.Bar._new()  # type: ignore # pylint: disable=no-member

        assert y is x is z
        assert x == y == z
        assert kwords['qux'] == x.qux == y.qux == z.qux

        self._teardown()


if __name__ == '__main__':
    pytest.main(args=[__file__])
