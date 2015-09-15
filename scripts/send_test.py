# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'

import sys
import logging
import can

from canberry.can_utils import make_sdo

_logger = logging.getLogger(__name__)

def main(args):
    bus = can.interface.Bus()
    msg = make_sdo(recipient=0x42, index=0x32)
    _l
    bus.send(msg)


if __name__ == '__main__':
    main(sys.argv[1:])
