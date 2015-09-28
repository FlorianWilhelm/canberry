from __future__ import absolute_import, division, print_function

import json
import math
import time

from flask import abort

from . import logic
from . import app
from .can_utils import Service
from .utils import add_timestamp


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/sensors')
def list_sensors():
    sensors = sorted(logic.Sensor.list_all().values())
    return json.dumps(sensors)


@app.route('/sensors/<sensor>')
def read_sensor(sensor):
    if logic.is_sensor_known(sensor):
        response = logic.read_sensor(sensor)
        add_timestamp(response)
        return json.dumps(response)
    else:
        return abort(404)


@app.route('/sensors/dummy1')
def read_dummy1():
    response = {Service.READ_PARAM: math.sin(0.5*time.time()),
                Service.READ_MIN: -1,
                Service.READ_MAX: 1,
                Service.READ_DEFAULT: 0,
                Service.READ_SCALE: 1}
    add_timestamp(response)
    return json.dumps(response)


@app.route('/sensors/dummy2')
def read_dummy2():
    response = {Service.READ_PARAM: 2*math.sin(time.time())+0.5,
                Service.READ_MIN: -1.5,
                Service.READ_MAX: 2.5,
                Service.READ_DEFAULT: 0,
                Service.READ_SCALE: 1}
    add_timestamp(response)
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
