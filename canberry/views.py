from __future__ import absolute_import, division, print_function

from . import app

@app.route('/')
def index():
    return app.send_static_file('index.html')
