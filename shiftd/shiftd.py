from functools import partial
from pathlib import Path
from typing import (
    Dict,
    Tuple,  # <- used in `get_app_and_ui` signature
)

import shiftd.logger
from shiftd.utils import make_singleton
from shiftd.logger import log_level

from adsk import (
    core as adskCore,
    fusion as adskFusion,
    cam as adskCam,
)


SELF_NAME = Path(__file__).name
LOG_FILE = Path.home() / '{}.log'.format(SELF_NAME)

debug = partial(shiftd.logger.log, file=str(LOG_FILE), level=log_level.DEBUG, ident=SELF_NAME)


def get_app_and_ui() -> "Tuple[adskCore.Application, adskCore.UserInterface]":
    app = adskCore.Application.get() or None
    ui = getattr(app, 'userInterface', None)

    debug('Got Fusion app ({!r}) and UI ({!r}) objects'.format(app, ui))
    return app, ui


# TODO: Catch error with decorator
def run(context: Dict[str, str]) -> None:
    debug('Addin started with a context: {!r}'.format(context))
    _, ui = get_app_and_ui()

    ui.messageBox('Hello, World!')


# TODO: Catch error with decorator
def stop(context: Dict[str, str]) -> None:
    debug('Addin stopped with a context: {!r}'.format(context))
