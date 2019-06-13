from functools import partial
from pathlib import Path
from typing import (
    Dict,
    Tuple,  # <- used in `get_app_and_ui` signature
)

import shiftd
CONFIG_FILE = '{}/cfg/dev.toml'.format(shiftd.__path__[0])  # type: ignore

import shiftd.logger
from shiftd.logger import log_level
from shiftd.utils import (
    make_singleton,
    parse_config,
    try_catch,
)

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


@make_singleton
class Server:

    @staticmethod
    def build_uri_from_3(proto: str, host: str, port: int) -> str:
        # TODO: semantic check of args
        return '{0}://{1}:{2!s}'.format(proto, host, port)


@try_catch
def run(context: Dict[str, str]) -> None:
    debug('Addin started with a context: {!r}'.format(context))

    shiftd.CONFIG = parse_config(CONFIG_FILE)

    if shiftd.CONFIG:
        _, ui = get_app_and_ui()
        ui.messageBox(Server.build_uri_from_3(shiftd.CONFIG['rpc']['proto'],
                                              shiftd.CONFIG['rpc']['host'],
                                              shiftd.CONFIG['rpc']['port'])
    )


@try_catch
def stop(context: Dict[str, str]) -> None:
    debug('Addin stopped with a context: {!r}'.format(context))
