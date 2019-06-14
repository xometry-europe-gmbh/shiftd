from collections import abc

from typing import (
    Any,
    Iterator,
)

# Support type checkers.
try:
    from adsk import (
        core as adskCore,
    )
except Exception:  # pylint: disable=broad-except
    pass


class iter(abc.Iterable):
    """Iterator for a common Fusion collections.

    """
    # pylint: disable=redefined-builtin

    _COUNT_PROPERTY = 'count'
    _ITEM_METHOD = 'item'

    ATTRIBUTES = frozenset([_COUNT_PROPERTY, _ITEM_METHOD])

    def __init__(self, obj: "adskCore.Base") -> None:
        if not all(hasattr(obj, attr) for attr in self.ATTRIBUTES):
            raise TypeError('Incompatible type of an object', obj)

        self.__index = 0
        self.__object = obj

    def __len__(self) -> int:
        return getattr(self.__object, self._COUNT_PROPERTY)

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        if self.__index < len(self):
            value = getattr(self.__object, self._ITEM_METHOD)(self.__index)

            self.__index += 1
            return value

        raise StopIteration

    def rewind(self) -> None:
        """Rewind the collection index.

        The next iterable value will be taken from the beginning.
        """
        self.__index = 0
