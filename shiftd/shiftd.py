from pathlib import Path
from typing import (
    Dict,
    Tuple,  # <- used in `get_app_and_ui` signature
)

import shiftd.logger
from shiftd.logger import LOG_LEVELS
from shiftd.utils import make_singleton

from adsk import (
    core as adskCore,
    fusion as adskFusion,
    cam as adskCam,
)


SELF_NAME = Path(__file__).name
LOG_FILE = Path.home() / '{}.log'.format(SELF_NAME)

def log(message: str, level: LOG_LEVELS = LOG_LEVELS.DEBUG) -> None:
    shiftd.logger.log(message, str(LOG_FILE), mode='w', level=level, ident=SELF_NAME)


def get_app_and_ui() -> "Tuple[adskCore.Application, adskCore.UserInterface]":
    app = adskCore.Application.get() or None
    ui = getattr(app, 'userInterface', None)

    log('Got Fusion app ({!r}) and UI ({!r}) objects'.format(app, ui))
    return app, ui


# TODO: Catch error with decorator
def run(context: Dict[str, str]) -> None:
    log('Addin started with a context: {!r}'.format(context))
    _, ui = get_app_and_ui()

    ui.messageBox('Hello, World!')


# TODO: Catch error with decorator
def stop(context: Dict[str, str]) -> None:
    log('Addin stopped with a context: {!r}'.format(context))
