# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
from canberry.can_utils import *


def test_make_mgmt_byte():
    mgmt_byte = make_mgt_byte(Service.code[Service.READ_PARAM], sync=True)
    assert bin(mgmt_byte) == '0b1110001'


def test_make_sdo_read():
    recipient = 16
    index = 1
    msg = make_sdo(recipient, index)
    assert bin(msg.arbitration_id) == '0b1010000011'
    # Check managment field
    assert msg.data[0] == make_mgt_byte(Service.code[Service.READ_PARAM])
    # Check reserved field
    assert msg.data[1] == 0
    # Check index fields
    assert msg.data[2] == 0
    assert msg.data[3] == 1
    # Check data fields
    assert msg.data[4] == 0
    assert msg.data[5] == 0
    assert msg.data[6] == 0
    assert msg.data[7] == 0


def test_make_sdo_write():
    recipient = 32
    index = 1024
    value = 1
    msg = make_sdo(recipient, index, value=value)
    assert bin(msg.arbitration_id) == '0b1100000011'
    # Check managment field
    assert msg.data[0] == make_mgt_byte(Service.code[Service.WRITE_PARAM])
    # Check reserved field
    assert msg.data[1] == 0
    # Check index fields
    assert msg.data[2] == 4
    assert msg.data[3] == 0
    # Check data fields
    assert msg.data[4] == 0
    assert msg.data[5] == 0
    assert msg.data[6] == 0
    assert msg.data[7] == 1


def test_bytes_to_int():
    bytes = bytearray([1, 0, 0, 0])
    result = bytes_to_int(bytes)
    assert result == 2**24
    bytes = bytearray([0, 0, 8, 0])
    result = bytes_to_int(bytes)
    assert result == 2**11
    bytes = bytearray([0, 0, 0, 0])
    result = bytes_to_int(bytes)
    assert result == 0
