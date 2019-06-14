import pytest

import shiftd.fusion as Fu


class TestFusion:
    # pylint: disable=blacklisted-name
    # pylint: disable=attribute-defined-outside-init

    def _setup(self) -> None:
        self.chars = ['@', 'S', 'U', 'N', '!']

        class Foo:

            def __init__(self, bar: str) -> None:
                self.bar = bar
                self.count = len(bar)

            def item(self, pos: int) -> str:
                return self.bar[pos]

        self.Foo = Foo

    def _teardown(self) -> None:
        pass

    def test_iter(self) -> None:
        self._setup()

        with pytest.raises(TypeError):
            Fu.iter(int(4))

        s = ''.join(self.chars)
        fu_iter = Fu.iter(self.Foo(s))

        assert len(fu_iter) == len(s) == len(self.chars)
        assert list(fu_iter) == self.chars

        fu_iter.rewind()
        assert list(fu_iter) == self.chars

        with pytest.raises(StopIteration):
            next(fu_iter)

        del self.Foo.item
        with pytest.raises(TypeError):
            Fu.iter(self.Foo(s))

        self._teardown()


if __name__ == '__main__':
    pytest.main(args=[__file__])
