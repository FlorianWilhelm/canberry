# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

import sys
import argparse

import canberry
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
    parser.add_argument(
        '-p',
        '--prod',
        dest='prod',
        action="store_true",
        default=False,
        help="production mode, disable debug")

    version = canberry.__version__
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='CANberry {ver}'.format(ver=version))
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    debug = False if args.prod else True
    app.run(debug=debug)


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
