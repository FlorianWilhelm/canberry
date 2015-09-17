========
CANberry
========

A small web app that displays sensor data and controls a small engine
connected to the Raspberry Pi with a controller area network (CAN) bus.

Description
===========

Development
-----------

Installation:

* Create a virtual environment `virtualenv venv` and activate it with
  `source venv/bin/activate`.
* Install all dependencies with `pip install -r requirements.txt`.
* Run `python setup.py develop` to install CANberry in your virtual environment.
* Run `canberry` from the command line to start the web application. Try
  `canberry -h` for help on more options.

Updating the javascript components with:

* Install *npm* with `sudo apt-get install nodejs`.
* Install *bower* with `sudo npm install -g bower`.
* Use `bower install -S` to install and update js dependencies like
  concise, ractive, jquery, flotcharts.

Configuration File
------------------

Create a configuration file .canrc with following content in your home directory::

    [default]
    interface = socketcan
    channel = can0

    [canberry]
    identifier = 16

The identifier is the default target address.

Note
====

This project has been set up using PyScaffold. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
