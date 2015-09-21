# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

import os
import logging
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

import can

from .can_utils import make_sdo, bytes_to_int, Service
from .utils import list_attributes


__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'

_logger = logging.getLogger(__name__)


class Sensor(object):
    """
    Namespace for convenient and consistent naming
    """
    SPEED = 'speed'
    DUMMY = 'dummy'
    code = {SPEED: 0x207E,
            DUMMY: 0xFFFF}

    @classmethod
    def list_all(cls):
        attrs = list_attributes(cls)
        return {k: v for k, v in attrs.items() if isinstance(v, basestring)}


def read_config():
    """
    Read the configuration files .canrc, can.conf etc. as defined by python
    can in order to retrieve all settings from the section [canberry].
    :return: dictionary
    """
    from can.util import CONFIG_FILES
    config = ConfigParser()
    config.read([os.path.expanduser(path) for path in CONFIG_FILES])
    if not config.has_section('canberry'):
        raise RuntimeError("Please add a section canberry to your CAN config!")
    return {key: int(val) for key, val in config.items('canberry')}


def read_sensor(sensor):
    """
    Retrieve the data from a sensor

    :param sensor: name of a sensor according to :obj:`inSensor`
    :return: sensor data as json dictionary
    """
    identifier = read_config()['identifier']
    bus = can.interface.Bus()
    services = [Service.READ_PARAM, Service.READ_DEFAULT, Service.READ_MIN,
                Service.READ_MAX, Service.READ_SCALE]

    response = dict()
    for service in services:
        msg = make_sdo(recipient=identifier,
                       index=Sensor.code[sensor],
                       service=service)
        _logger.debug("Sending {} message to {}...".format(service, sensor))
        if bus.send(msg) < 0:
            raise RuntimeError('No message received')
        _logger.debug("Waiting for message...")
        reply = bus.recv()
        _logger.debug("Message received:\n{}".format(reply))
        response[service] = bytes_to_int(reply.data[4:8])

    return response
