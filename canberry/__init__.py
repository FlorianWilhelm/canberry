# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

from flask import Flask
app = Flask(__name__)

from flask.ext.bower import Bower
Bower(app)

from . import views
