from __future__ import absolute_import, division, print_function

import json
import math
import time

from flask import abort

from . import logic
from . import app
from .can_utils import Service


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/sensors')
def list_sensors():
    sensors = logic.Sensor.list_all().values()
    return json.dumps(sensors)


@app.route('/sensors/<sensor>')
def read_sensor(sensor):
    known_sensors = logic.Sensor.list_all()
    for _, v in known_sensors.items():
        if v == sensor:
            return json.dumps(logic.read_sensor(sensor))
    return abort(404)


@app.route('/sensors/dummy')
def read_dummy():
    response = {Service.READ_PARAM: 0.2*math.sin(time.time()),
                Service.READ_MIN: -1,
                Service.READ_MAX: 1,
                Service.READ_DEFAULT: 0,
                Service.READ_SCALE: 1}
    return json.dumps(response)
