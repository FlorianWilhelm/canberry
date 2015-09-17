from __future__ import absolute_import, division, print_function

import math
import time

from . import app
from .logic import get_sensor

from flask import abort
from .logic import Sensor


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/sensors/<sensor>')
def sensors(sensor):
    known_sensors = Sensor.list_all()
    for _, v in known_sensors.items():
        if v == sensor:
            return get_sensor(sensor)
    return abort(404)


@app.route('/sensors/dummy')
def dummy():
    return str(0.2*math.sin(time.time()))
