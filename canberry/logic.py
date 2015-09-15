# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

import os
import logging
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

from .can_utils import make_sdo, bytes_to_int

import can

__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'

_logger = logging.getLogger(__name__)


class sensors(object):
    SPEED = 0x207E


def read_config():
    from can.util import CONFIG_FILES
    config = ConfigParser()
    config.read([os.path.expanduser(path) for path in CONFIG_FILES])
    if not config.has_section('canberry'):
        raise RuntimeError("Please add a section canberry to your CAN config!")
    return {key: val for key, val in config.items('canberry')}


def get_speed():
    identifier = read_config()['identifier']
    msg = make_sdo(recipient=identifier, index=sensors.SPEED)
    bus = can.interface.Bus()
    _logger.debug("Sending message to retrieve rotational speed...")
    if bus.send(msg) < 0:
        _logger.debug("Message not sent!")
    else:
        _logger.debug("Message sent!")
    _logger.debug("Waiting for message...")
    reply = bus.recv()
    _logger.debug("Message received:\n{}".format(reply))
    return bytes_to_int(reply.data[4:8])
