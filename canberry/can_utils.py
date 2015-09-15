from __future__ import print_function, absolute_import, division

import can


class service(object):
    NO_SERVICE = 0
    READ_PARAM = 1
    WRITE_PARAM = 2
    WRITE_PARAM_VOLATILE = 3
    READ_MIN = 4
    READ_MAX = 5
    READ_DEFAULT = 6
    READ_SCALE = 7
    READ_ATTR = 8


def make_mgt_byte(service, sync=False):
    msg = service + 3*16
    if sync:
        msg += 64
    return msg


def make_sdo(recipient, index, value=None, sync=False):
    read = True if value is None else False
    arb_id = 8 * recipient + 512 + 3
    if read:
        mgmt_byte = make_mgt_byte(service.READ_PARAM, sync)
        value = 0
    else:
        mgmt_byte = make_mgt_byte(service.WRITE_PARAM, sync)
    index_high = index >> 8  # first two hex digits
    index_low = index - (index_high << 8)  # last two hex digits
    value = '{:08x}'.format(value)  # padding with 0 to 4 bytes
    # Split into 1 byte pieces and convert to int
    value = [int(value[i:i+2]) for i in range(0, len(value), 2)]
    data = [mgmt_byte, 0, index_high, index_low] + value
    msg = can.Message(arbitration_id=arb_id, data=data, extended_id=False)
    return msg
