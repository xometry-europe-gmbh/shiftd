import argparse
import logging

from typing import (
    Any,
    Dict,
    Optional,
)


__version__ = '0.1.0'
__release__ = __version__

DEBUG = False

# Type definitions ==>
CONFIG_TYPE = Optional[Dict[str, Any]]
# <==

ARGS: Optional[argparse.Namespace] = None
CONFIG: CONFIG_TYPE = None

LOG_FMT = '%(levelname)s: %(name)s [%(process)d] {%(filename)s@L%(lineno)d}: %(message)s'
LOG_LVL = logging.INFO

SHIFTD_DESC = 'Shift GmbH Dispatcher'
SHIFTAPP_DESC = 'Shift GmbH Logistic App'

RPC_URI: Optional[str] = None
