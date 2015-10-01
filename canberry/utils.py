# -*- coding: utf-8 -*-
"""
Additional utilities unrelated to everyting else
"""
from __future__ import print_function, absolute_import, division

import math
import time

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
