"use strict";

// Settings
var updateInterval = 100;
var maxNumOfElements = 1000;

// Module pattern to store sensor data
// http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html
var sensorData = (function () {
    var plot;
    var interval = maxNumOfElements * updateInterval;
    var data = []; // private
    var pub = {}; // public object - returned at end of module

    pub.addData = function(tuple) {
        if (data.length > maxNumOfElements) {
            data.shift();
        }
        data.push(tuple);
    };

    pub.clearData = function() {
        data = [];
    };

    pub.initPlot = function (min, max) {
        plot = $.plot("#sensor-plot", [[0, 0]], {
            yaxis: {
                min: min,
                max: max
            },
            xaxis: {
                show: false,
                min: 0,
                max: interval
            }
        });
    };

    // private function to restict data to plotting interval
    function prepareData(data) {
        var x_max = data[data.length-1][0];
        var res = data.filter(function(elem, idx) {
            return elem[0] >= x_max - interval;
        })
        res = res.map(function(elem, idx){
            return [interval - (x_max - elem[0]), elem[1]]
        });
        return res;
    }

    pub.plotData = function() {
        var points = prepareData(data);
        plot.setData([points]);
        plot.draw();
    };

    return pub; // expose externally
}());

var sensorSelector = (function () {
    var currSensor; // private
    var sensors = []; // private
    var pub = {}; // public object - returned at end of module

    pub.initSensors = function (list) {
        assert(!isArrayEmpty(list));
        sensors = list;
        currSensor = list[0];
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

function assert(condition, message) {
    if (!condition) {
        message = message || "Assertion failed";
        if (typeof Error !== "undefined") {
            throw new Error(message);
        }
        throw message; // Fallback
    }
}

function readSensor() {
    return $.when( $.getJSON('./sensors/dummy') ).done(function(data, status) {
        sensorData.addData([$.now(), data.parameter])});
}

function initSensors() {
    return $.when( $.getJSON('./sensors') ).done(function(data, status) {
    sensorSelector.initSensors(data)});
}

function updateGraph() {
    $.when( readSensor() ).done(function(data, status) {
        sensorData.plotData();
        $('#sensor-value').text(data.parameter);
        });
}

function isArrayEmpty(array) {
    // the array is defined and has at least one element
    return typeof array === 'undefined' || array.length == 0;
}

// initialization, starting of ractive.js and refresh interval
var ractive;
$( document ).ready(function() {
    $.when( initSensors(), readSensor() ).done(function(sensors, data) {
        ractive = new Ractive({
          // The `el` option can be a node, an ID, or a CSS selector.
          el: '#container',
          // We could pass in a string, but for the sake of convenience
          // we're passing the ID of the <script> tag above.
          template: '#template',
          // Here, we're passing in some initial data
          data: {sensors: sensorSelector.listSensors(),
                 currSensor: sensorSelector.getCurrSensor()}
        });
        sensorData.initPlot(data.minimum, data.maximum);
        setInterval(updateGraph, updateInterval);
    });
});
