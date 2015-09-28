# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

import time

__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'


def list_attributes(obj):
    """
    Lists all attributes of an object or class

    :param obj: object or class
    :return: dictionary of user-defined attributes
    """
    return {k: v for k, v in vars(obj).items() if not k.startswith('__')}


def add_timestamp(dct):
    """
    Adds a timestamp attribute in miliseconds to a dictionary

    :param dct: dictionary
    """
    dct['timestamp'] = time.time() * 1000
