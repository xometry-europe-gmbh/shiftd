#!/usr/bin/env python3.7

from typing import (
    Iterable,
)

import pytest

from shiftd.utils import make_singleton


class TestUtils:
    # pylint: disable=blacklisted-name
    # pylint: disable=attribute-defined-outside-init

    def _setup(self) -> None:
        self.args = [1, 17, 29]
        self.kwords = {'word': 'Apple', 'Name': 'Chloe', 'qux': 'LUX'}

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

        x = self.Bar(*self.args, **self.kwords)
        y = self.Bar._new()  # type: ignore # pylint: disable=no-member
        z = self.Bar._new()  # type: ignore # pylint: disable=no-member

        assert y is x is z
        assert x == y == z
        assert self.kwords['qux'] == x.qux == y.qux == z.qux

        self._teardown()

    def test_make_singleton_new_method(self) -> None:
        self._setup()

        assert self.Bar._new() is None  # type: ignore # pylint: disable=no-member

        self.Bar()
        assert isinstance(self.Bar._new(), self.Bar)  # type: ignore # pylint: disable=no-member

        self._teardown()


if __name__ == '__main__':
    pytest.main(args=[__file__])
