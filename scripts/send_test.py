#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'

import sys
import logging
import can

from canberry.can_utils import make_sdo
from canberry.logic import Sensor

_logger = logging.getLogger(__name__)


def main(args):
    bus = can.interface.Bus()
    msg = make_sdo(recipient=42, index=Sensor.SPEED)
    _logger.info("Sending message...")
    if bus.send(msg) < 0:
        _logger.info("Message not sent!")
    else:
        _logger.info("Message sent!")
    _logger.info("Waiting for message...")
    answer = bus.recv()
    _logger.info("Message received:\n{}".format(answer))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    main(sys.argv[1:])
