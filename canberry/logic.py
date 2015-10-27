# -*- coding: utf-8 -*-
"""
High-level functions to read and write a sensor of the MOVIDRIVE traction
converter
"""
from __future__ import print_function, absolute_import, division

import logging

import can
from .can_utils import make_sdo, bytes_to_int, Service
from .utils import list_attributes, read_config


__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'

_logger = logging.getLogger(__name__)


class Sensor(object):
    """
    Namespace for convenient and consistent naming
    """
    SPEED = 'speed'
    DUMMY1 = 'dummy1'
    DUMMY2 = 'dummy2'
    code = {SPEED: 0x207E,
            DUMMY1: 0xFFFF,
            DUMMY2: 0xFFFF}

    @classmethod
    def list_all(cls):
        attrs = list_attributes(cls)
        sensors = {k: v for k, v in attrs.items() if isinstance(v, basestring)}
        if not read_config()['debug']:
            sensors = {k: v for k,v in sensors.items()
                       if not k.startswith('DUMMY')}
        return sensors


def read_sensor(sensor):
    """
    Retrieve the data from a sensor

    :param sensor: name of a sensor according to :obj:`inSensor`
    :return: sensor data as dictionary
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
            raise RuntimeError('Error sending message')
        _logger.debug("Waiting for message...")
        reply = bus.recv()
        _logger.debug("Message received:\n{}".format(reply))
        response[service] = bytes_to_int(reply.data[4:8])

    return response


def is_sensor_known(sensor):
    """
    Check if sensor is known

    :param sensor: sensor as string
    :return: boolean
    """
    for known_sensor in Sensor.list_all().values():
        if sensor == known_sensor:
            return True
    return False


def write_sensor(sensor, value, volatile=False):
    """
    Write a value to a sensor

    :param sensor: name of a sensor according to :obj:`inSensor`
    :param value: value to write
    :param volatile: write parameter volatile as boolean
    """
    identifier = read_config()['identifier']
    bus = can.interface.Bus()
    if volatile:
        service = Service.WRITE_PARAM_VOLATILE
    else:
        service = Service.WRITE_PARAM
    msg = make_sdo(recipient=identifier,
                   index=Sensor.code[sensor],
                   service=service,
                   value=value)
    _logger.debug("Sending {} message with value {} message "
                  "to {}...".format(service, value, sensor))
    if bus.send(msg) < 0:
        raise RuntimeError('Error sending message')
