# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'


def list_attributes(obj):
    """
    Lists all attributes of an object or class

    :param obj: object or class
    :return: dictionary of user-defined attributes
    """
    return {k: v for k, v in vars(obj).items() if not k.startswith('__')}
