import webbrowser

from functools import partial
from pathlib import Path
from typing import (
    Dict,
    Optional,
    Tuple,  # <- used in `get_app_and_ui` signature
)

import shiftd
CONFIG_FILE = '{}/cfg/dev.toml'.format(shiftd.__path__[0])  # type: ignore

import shiftd.fusion as Fu
import shiftd.logger
from shiftd.logger import log_level
from shiftd.utils import (
    make_singleton,
    parse_config,
    try_catch,
)

import zerorpc

from adsk import (
    core as adskCore,
)


SELF_NAME = Path(__file__).name
LOG_FILE = Path.home() / '{}.log'.format(SELF_NAME)

_log_kwargs = {'file': str(LOG_FILE), 'ident': SELF_NAME}
#
dbg = partial(shiftd.logger.log, level=log_level.DEBUG, **_log_kwargs)
error = partial(shiftd.logger.log, level=log_level.ERROR, **_log_kwargs)

FUSION_URI_f = 'fusion360://command=open&file={!s}'


def get_app_and_ui() -> "Tuple[adskCore.Application, adskCore.UserInterface]":
    app = adskCore.Application.get() or None
    ui = getattr(app, 'userInterface', None)

    dbg('Got Fusion app ({0!r}) and UI ({1!r}) objects'.format(app, ui))
    return app, ui


@make_singleton
class Dispatcher:
    # pylint: disable=no-self-use

    def __init__(self) -> None:
        self.__app, self.__ui = get_app_and_ui()

        if not self.__app:
            raise RuntimeError("Fusion app object can't be acquired")
        if not self.__ui:
            raise RuntimeError("Fusion UI object can't be acquired")

    @property
    def app(self) -> adskCore.Application:
        return self.__app

    @property
    def ui(self) -> adskCore.UserInterface:
        return self.__ui

    ##
    # RPC-methods to dispatch
    #
    # Methods that using Fusion API explicitly have a such signature: `def fusion_*(self, *)`
    # ==>
    def hello(self, subject: str) -> None:
        self.__ui.messageBox('Hello, {}!'.format(subject))

    def quit(self) -> None:
        server = Server._new()  # type: ignore # pylint: disable=no-member
        if server:
            server.shutdown()

    def open_local_file(self, file: str) -> None:
        if file:
            if Path(file).is_file():
                uri = FUSION_URI_f.format(file)
                dbg('Sending URI to browser: {!r}'.format(uri))

                webbrowser.open(uri)
            else:
                error('Invalid file or path: {!s}'.format(file))

    def fusion_close_all(self) -> None:
        fu_iter = Fu.iter(self.__app.documents)

        for index, doc in enumerate(fu_iter):
            name = doc.name
            success = doc.close(False)  # (saveChanges: bool) -> bool

            dbg('Trying to close a Fusion document named {0!r} [{1!s}, {2!s}) -> {3!r}'
                .format(name, index, len(fu_iter), success))
    # <==
    ##


@make_singleton
class Server:

    @staticmethod
    def build_uri_from_3(proto: str, host: str, port: int) -> str:
        # TODO: semantic check of args
        return '{0}://{1}:{2!s}'.format(proto, host, port)

    def __init__(self, dispatcher: Dispatcher) -> None:
        self.__server = zerorpc.Server(dispatcher)
        self.__server.debug = True

        self.__uri = None  # type: Optional[str]

    @property
    def uri(self) -> str:
        return self.__uri

    @uri.setter
    def uri(self, rpc_uri: str) -> None:
        if not rpc_uri:
            raise ValueError('Valid URI must be passed', rpc_uri)
        self.__uri = rpc_uri

    def start(self) -> None:
        if isinstance(self.__server, zerorpc.Server) and self.__uri:
            dbg('Starting RPC server {0!r} on {1!r}'.format(self.__server, self.__uri))
            self.__server.bind(self.__uri)
            self.__server.run()

    def shutdown(self) -> None:
        if isinstance(self.__server, zerorpc.Server):
            dbg('Shutting down the RPC server: {!r}'.format(self.__server))

            self.__server.stop()
            self.__server.close()


@try_catch
def run(context: Dict[str, str]) -> None:
    dbg('Addin started with a context: {!r}'.format(context))

    shiftd.CONFIG = parse_config(CONFIG_FILE)

    if shiftd.CONFIG:
        dispatcher = Dispatcher()

        server = Server(dispatcher)
        server.uri = Server.build_uri_from_3(shiftd.CONFIG['rpc']['proto'],
                                             shiftd.CONFIG['rpc']['host'],
                                             shiftd.CONFIG['rpc']['port'])
        server.start()
        server.shutdown()  # im dumb


@try_catch
def stop(context: Dict[str, str]) -> None:
    dbg('Addin stopped with a context: {!r}'.format(context))

# FIXME: zerorpc import produces `syntax error in type comment` error at the last line
