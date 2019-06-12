import argparse
import traceback

from functools import partial
from pathlib import Path
from typing import (
    Any,
    Callable,
)

import shiftd.logger
from shiftd.logger import log_level


SELF_NAME = Path(__file__).name
LOG_FILE = Path.home() / '{}.log'.format(SELF_NAME)

error = partial(shiftd.logger.log, file=str(LOG_FILE), level=log_level.ERROR, ident=SELF_NAME)


def make_singleton(cls):  # type: ignore

    class wrp(cls):
    # pylint: disable=bad-classmethod-argument
    #
        def __new__(c, *args: Any, **kwargs: Any) -> "wrp":
        # pylint: disable=unused-argument
        #
            instance = getattr(c, '_{}__instance'.format(c.__name__), None)

            if instance is None:
                instance = super().__new__(c)
                c.__instance = instance
            elif not isinstance(instance, c):
                raise TypeError('Incompatible type', type(instance))

            return instance

        @classmethod
        def _new(c) -> "wrp":
            return c.__instance

    return wrp


class try_catch:

    def __init__(self, func: Callable) -> None:
        self.__func = func

    def __call__(self, *args: Any, **kwargs: Any) -> None:
    # pylint: disable=broad-except
    #
        try:
            return self.__func(*args, **kwargs)
        except Exception:
            error('`{0!r}` failed for args={1!r} and kwargs={2!r}'
                  .format(self.__func, args, kwargs))
            error('{!s}'.format(traceback.format_exc()))


class CustomHelpFormatter(argparse.HelpFormatter):

    def _format_action(self, action: argparse.Action) -> str:
    # pylint: disable=attribute-defined-outside-init
    #
        if isinstance(action, argparse._SubParsersAction):
            self._subaction_max_length = max(
                len(i) for i in [self._format_action_invocation(a)
                                 for a in action._get_subactions()]
            )

        if isinstance(action, argparse._SubParsersAction._ChoicesPseudoAction):
            subaction = self._format_action_invocation(action)
            width = self._subaction_max_length
            help_text = self._expand_help(action) if action.help else str()

            return '{indent_first}{:{width}}{indent_help}{}\n'.format(
                subaction, help_text,
                indent_first=' '*2, width=width, indent_help=' '*10
            )
        elif isinstance(action, argparse._SubParsersAction):
            return '\n{}'.format(''.join(
                self._format_action(a) for a in action._get_subactions()
            ))
        else:
            return super()._format_action(action)
