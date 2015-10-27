# -*- coding: utf-8 -*-
"""
The command line interface for canberry
"""
from __future__ import print_function, absolute_import, division

import sys
import argparse

import canberry
from .utils import read_config
from canberry import app

__author__ = 'Florian Wilhelm'
__copyright__ = 'Florian Wilhelm'


def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as dictionary
    """
    parser = argparse.ArgumentParser(
        description="CANberry, webapp for raspberry pi with CAN bus")
    version = canberry.__version__
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='CANberry {ver}'.format(ver=version))
    return parser.parse_args(args)


def main(args):
    parse_args(args)
    cfg = read_config()
    host = '0.0.0.0' if cfg['external'] else None
    app.run(debug=cfg['debug'], host=host)


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
