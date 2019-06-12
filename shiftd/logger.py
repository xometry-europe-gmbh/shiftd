from datetime import datetime as dt
from enum import Enum

from typing import (
    Optional,
)


class log_level(Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


def log(message: str, file: str, mode: str = 'a', level: log_level = log_level.NOTSET,
         ident: Optional[str] = None
) -> None:
#
    with open(file, mode) as fd:
        fd.write('{0} |><| {1}{3}: {2}\n'
                 .format(dt.now(), level.name, message, ' {{{}}}'.format(ident) if ident else '')
        )
