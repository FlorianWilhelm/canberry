"""
Views of the flask application
"""
from __future__ import absolute_import, division, print_function

import json
import math
import time

from flask import abort, request

from . import logic
from . import app
from .utils import add_timestamp, DummySensor, static_vars


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/sensors')
def list_sensors():
    sensors = sorted(logic.Sensor.list_all().values())
    return json.dumps(sensors)


@app.route('/sensors/<sensor>', methods=['GET'])
def read_sensor(sensor):
    if logic.is_sensor_known(sensor):
        try:
            response = logic.read_sensor(sensor)
            add_timestamp(response)
            return json.dumps(response)
        except Exception as e:
            return str(e), 500
    else:
        return abort(404)


@app.route('/sensors/<sensor>', methods=['POST'])
def write_sensor(sensor):
    if logic.is_sensor_known(sensor):
        try:
            logic.write_sensor(sensor, request.form['newValue'])
        except Exception as e:
            return str(e), 500
        return '', 204
    else:
        return abort(404)


@static_vars(dummy=DummySensor())
@app.route('/sensors/dummy1', methods=['GET', 'POST'])
def handle_dummy1():
    if request.method == 'GET': # read
        response = handle_dummy1.dummy.read()
        add_timestamp(response)
        return json.dumps(response)
    else: # write
        handle_dummy1.dummy.set(request.form['newValue'])
        return '', 204


@static_vars(dummy=DummySensor(trans=0.5, scale=1.5))
@app.route('/sensors/dummy2', methods=['GET', 'POST'])
def handle_dummy2():
    if request.method == 'GET': # read
        response = handle_dummy2.dummy.read()
        add_timestamp(response)
        return json.dumps(response)
    else: # write
        handle_dummy2.dummy.set(request.form['newValue'])
        return '', 204
