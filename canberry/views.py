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
    if logic.is_sensor_known(sensor):
        return json.dumps(logic.read_sensor(sensor))
    else:
        return abort(404)


@app.route('/sensors/dummy1')
def read_dummy1():
    response = {Service.READ_PARAM: math.sin(0.5*time.time()),
                Service.READ_MIN: -1,
                Service.READ_MAX: 1,
                Service.READ_DEFAULT: 0,
                Service.READ_SCALE: 1}
    return json.dumps(response)


@app.route('/sensors/dummy2')
def read_dummy2():
    response = {Service.READ_PARAM: math.sin(2.0*time.time()),
                Service.READ_MIN: -1,
                Service.READ_MAX: 1,
                Service.READ_DEFAULT: 0,
                Service.READ_SCALE: 1}
    return json.dumps(response)


@app.route('/sensors/<sensor>/<int:value>')
def write_sensor(sensor, value):
    if logic.is_sensor_known(sensor):
        try:
            logic.write_sensor(sensor, value)
        except:
            raise
            # return json.dumps({'status': 'error'})
        return json.dumps({'status': 'ok'})
    else:
        return abort(404)
