# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'

from canberry.utils import *


def test_list_attributes():
    class A(object):
        a = 1
        b = 2

    attr = list_attributes(A)
    exp_result = {'a': 1, 'b': 2}
    assert attr == exp_result
