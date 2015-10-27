# -*- coding: utf-8 -*-
"""
Additional utilities
"""
from __future__ import print_function, absolute_import, division

import os
import math
import time

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

from .can_utils import Service

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


def static_vars(**kwargs):
    """
    Decorator for adding a static variable to a function

    :param kwargs: initializations of the static variables
    """
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


class DummySensor(object):
    """
    A dummy sensor for test purposes
    """
    def __init__(self, trans=0., scale=1.):
        self.trans = trans
        self.scale = scale
        self.freq = 1.

    def read(self):
        response = {
            Service.READ_PARAM: (self.scale*math.sin(self.freq*time.time()) +
                                 self.trans),
            Service.READ_MIN: -self.scale + self.trans,
            Service.READ_MAX: self.scale + self.trans,
            Service.READ_DEFAULT: self.trans,
            Service.READ_SCALE: 1.}
        return response

    def set(self, freq):
        self.freq = float(freq)


def str2bool(txt):
    """
    Convert a string to a boolean

    :param txt: string object
    :return: boolean
    """
    if txt.lower() in ['1', 'true', 'yes', 'y']:
        return True
    elif txt.lower() in ['0', 'false', 'no', 'n']:
        return False
    else:
        raise ValueError("Can't convert \"{}\" to a boolean".format(txt))


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
    cfg = {key: val for key, val in config.items('canberry')}
    # Map configuration values to the right data type and set defaults
    cfg['identifier'] = int(cfg.get('identifier', '0'))
    cfg['external'] = str2bool(cfg.get('external', 'true'))
    cfg['debug'] = str2bool(cfg.get('debug', 'false'))
    return cfg
