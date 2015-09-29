# -*- coding: utf-8 -*-
"""
Implementation of the protocol for the MOVIDRIVE traction converter of
SEW EURODRIVE
"""
from __future__ import print_function, absolute_import, division

import struct

import can


class Service(object):
    """
    Namespace for convenient and consistent naming
    """
    NO_SERVICE = 'no_service'
    WRITE_PARAM = 'write_parameter'
    WRITE_PARAM_VOLATILE = 'write_parameter_volatile'
    READ_PARAM = 'parameter'
    READ_MIN = 'minimum'
    READ_MAX = 'maximum'
    READ_DEFAULT = 'default'
    READ_SCALE = 'scale'
    READ_ATTR = 'attribute'
    code = {NO_SERVICE: 0,
            READ_PARAM: 1,
            WRITE_PARAM: 2,
            WRITE_PARAM_VOLATILE: 3,
            READ_MIN: 4,
            READ_MAX: 5,
            READ_DEFAULT: 6,
            READ_SCALE: 7,
            READ_ATTR: 8}


def make_mgt_byte(service, sync=False):
    """
    Creates the management byte according to the protocol

    :param service: Service code as defined in :obj:`~.Service`
    :param sync: boolean if synchronized mode should be used
    :return: integer
    """
    msg = service + 3*16
    if sync:
        msg += 64
    return msg


def bytes_to_int(bytes):
    """
    Convert a bytearray to an integer

    :param bytes: bytearray
    :return: integer
    """
    return struct.unpack('>I', ''.join([chr(x) for x in bytes]))[0]


def make_sdo(recipient, index, service=None, value=None, sync=False):
    """
    Creates a Service Data Object message

    :param recipient: the recipient as integer
    :param index: integer for the sensor
    :param service: requested service from :obj:`~.Service `
    :param value: None to read a value otherwise write value
    :param sync: Synchronized protocol
    :return: Service Data Object message
    """
    if service is None:
        read = True if value is None else False
        if read:
            service = Service.READ_PARAM
        else:
            service = Service.WRITE_PARAM
    if value is None:
        if service in [Service.WRITE_PARAM, Service.WRITE_PARAM_VOLATILE]:
            raise RuntimeError("No value set for writing sensor!")
        value = 0
    mgmt_byte = make_mgt_byte(Service.code[service], sync)
    index_high = index >> 8  # first two hex digits
    index_low = index - (index_high << 8)  # last two hex digits
    value = '{:08x}'.format(value)  # padding with 0 to 4 bytes
    # Split into 1 byte pieces and convert to int
    value = [int(value[i:i+2]) for i in range(0, len(value), 2)]
    data = [mgmt_byte, 0, index_high, index_low] + value
    arb_id = 8 * recipient + 512 + 3
    return can.Message(arbitration_id=arb_id, data=data, extended_id=False)
