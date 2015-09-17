from __future__ import absolute_import, division, print_function

from . import app
from .logic import get_sensor

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/sensors/<sensor>')
def sensors(sensor):
    return get_sensor(sensor)
