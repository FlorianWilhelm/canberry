"use strict";

// Settings
var updateInterval = 100;
var maxNumOfElements = 1000;
var errorDisplayTime = 5000;

// Module pattern to store sensor data
// http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html
var sensorData = (function() {
    var plot;
    var points = [];
    var lastData;
    var interval = maxNumOfElements * updateInterval;
    var pub = {}; // public object - returned at end of module

    /* Private functions */

    function addData(data) {
        lastData = data;
        points.push([data.timestamp, data.parameter/data.scale])
        while (points.length > maxNumOfElements) {
            points.shift();
        }
    }

    // restict data to plotting interval
    function transformedPoints() {
        var x_max = points[points.length-1][0];
        var res = points.filter(function(elem, idx) {
            // check line segment delimiters
            if (elem === null) {
                return true;
            }
            return elem[0] >= x_max - interval;
        })
        res = res.map(function(elem, idx){
            // check line segment delimiters
            if (elem === null) {
                return null;
            }
            return [interval - (x_max - elem[0]), elem[1]]
        });
        return res;
    }

    function initPlot() {
        points.splice(points.length-1, 0, null) // start a new line segment
        plot = $.plot("#sensor-plot", [points], {
            yaxis: {
                min: pub.getMinimum(),
                max: pub.getMaximum()
            },
            xaxis: {
                show: false,
                min: 0,
                max: interval
            }
        });
    }

    /* Public functions */

    pub.updateSensor = function() {
        var url = './sensors/' + sensorSelector.getCurrSensor();
        return $.getJSON(url).then(addData);
    }

    pub.updatePlot = function() {
        plot.setData([transformedPoints()]);
        plot.draw();
    };

    pub.startNewSensor = function() {
        return sensorData.updateSensor().then(initPlot);
    };

    pub.getSensorValue = function() {
        return points[points.length-1][1];
    };

    pub.setSensorValue = function(form) {
        var url = './sensors/' + sensorSelector.getCurrSensor();
        return $.post(url, {newValue: form.newValue.value*lastData.scale});
    };

    pub.getSensorData = function() {
        return lastData;
    };

    pub.getDefault = function() {
        return lastData.default / lastData.scale
    };

    pub.getMinimum = function() {
        return lastData.minimum / lastData.scale
    };

    pub.getMaximum = function() {
        return lastData.maximum / lastData.scale
    };

    return pub; // expose externally
}());

// Module pattern to store all sensors and the currently selected one
var sensorSelector = (function() {
    var currSensor; // private
    var sensors = []; // private
    var pub = {}; // public object - returned at end of module

    /* Public functions */

    pub.initSensors = function() {
        return $.getJSON('./sensors').then(function(data, status) {
            assert( !isArrayEmpty(data) );
            sensors = data;
            currSensor = data[0];
        });
    };

    pub.getCurrSensor = function() {
        return currSensor;
    };

    pub.setCurrSensor = function(sensor) {
        assert(sensors.indexOf(sensor) > -1);
        currSensor = sensor;
    };

    pub.listSensors = function() {
        return sensors;
    };

    return pub; // expose externally
}());

// Handler for error messages and alerts
var errorHandler = (function() {
    var timeout;
    var pub = {}; // public object - returned at end of module

    /* Private functions */

    function displayAlert(message) {
        ractive.set('error', false);
    }

    /* Public functions */

    pub.handle = function(msg) {
        ractive.set('errorMsg', msg.responseText);
        if (!ractive.get('error')) {
            ractive.set('error', true);
        }
        clearTimeout(timeout);
        timeout = setTimeout(displayAlert, errorDisplayTime);
    };

    return pub; // expose externally
}());

function assert(condition, message) {
    if (!condition) {
        message = message || "Assertion failed";
        if (typeof Error !== "undefined") {
            throw new Error(message);
        }
        throw message; // Fallback
    }
}

function isArrayEmpty(array) {
    // the array is undefined or has no elements
    return typeof array === 'undefined' || array.length == 0;
}

function refreshApp() {
    sensorData.updateSensor().then(sensorData.updatePlot).done(function() {
        ractive.set('sensorValue', sensorData.getSensorValue())
    });

}

// Set up Ractive.js and event proxies
function initRactive() {
    ractive = new Ractive({
        // Where to render the template as node, an ID, or a CSS selector
        el: '#container',
        // ID of a script tag as template defined in index.html
        template: '#template',
        // Initial data for all template parameters
        data: {sensors: sensorSelector.listSensors(),
               currSensor: sensorSelector.getCurrSensor(),
               sensorValue: sensorData.getSensorValue(),
               sensorDefault: sensorData.getDefault(),
               sensorMin: sensorData.getMinimum(),
               sensorMax: sensorData.getMaximum(),
               error: false,
               errorMsg: ''}
    });
    ractive.on('change-sensor', function (event) {
        sensorSelector.setCurrSensor(event.context);
        ractive.set('currSensor', event.context);
        ractive.set('sensorMin', sensorData.getMinimum());
        ractive.set('sensorMax', sensorData.getMaximum());
        sensorData.startNewSensor();
    });
}

// Initialization, starting of ractive.js and refresh interval
var ractive;
$(document).ready(function() {
    $.ajaxSetup({
        "error": errorHandler.handle
    });
    sensorSelector.initSensors().then(
        sensorData.updateSensor).done(function() {
            initRactive();
            sensorData.startNewSensor();
            setInterval(refreshApp, updateInterval);
        })
});
