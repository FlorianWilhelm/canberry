========
CANberry
========

A small web app that displays sensor data and controls a `MOVIDRIVE Antriebsumrichter
<http://www.sew-eurodrive.at/produkt/antriebsumrichter-movidrive.htm>`_
(traction converter) of SEW EURODRIVE connected to the `Raspberry Pi
<https://www.raspberrypi.org/>`_ with the help of a controller area network
(CAN) bus.

Manuals
-------

* `MOVIDRIVE Serielle Kommunikation (10531602) <http://download.sew-eurodrive.com/download/pdf/10531602.pdf>`_
* `MOVIDRIVE Handbuch (09191607) <http://download.sew-eurodrive.com/download/pdf/09191607.pdf>`_
* `MOVIDRIVE Betriebsanleitung (10532609) <http://download.sew-eurodrive.com/download/pdf/10532609.pdf>`_
* `MOVIDRIVE Operating Instruction (10532617) <http://download.sew-eurodrive.com/download/pdf/10532617.pdf>`_

Installation
============

Just use pip to install CANberry and all its dependencies::

    pip install canberry


Configuration
=============

Create a configuration file .canrc with following content in your home directory::

    [default]
    interface = socketcan
    channel = can0

    [canberry]
    identifier = 16
    # Is server externally visible? 'true' or 'false'
    external = true
    # Run the server in debug mode? 'true' or 'false'
    debug = false

The identifier is the default target address. One should note that running an
externally visible server in debug mode is not recommended!

Development
===========

Installation:

* Create a virtual environment `virtualenv venv` and activate it with
  `source venv/bin/activate`.
* Install all dependencies with `pip install -r requirements.txt`.
* Run `python setup.py develop` to install CANberry in your virtual environment.
* Run `canberry` from the command line to start the web application. Try
  `canberry -h` for help on more options.

In order to update the Javascript components shipped with CANberry with:

* Install *npm* with `sudo apt-get install nodejs`.
* Install *bower* with `sudo npm install -g bower`.
* Use `bower install -S` to install and update js dependencies like
  concise, ractive, jquery, flotcharts.

Credits
=======

This project uses following libraries:

* `jQuery <https://jquery.com/>`_
* `Concise CSS <http://concisecss.com/>`_
* `Ractive.js <http://www.ractivejs.org/>`_
* `Flot <http://www.flotcharts.org/>`_
* `python-can <https://python-can.readthedocs.org/>`_


Note
====

This project has been set up using PyScaffold. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
