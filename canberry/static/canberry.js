"use strict";

// Settings
var updateInterval = 100;
var maxNumOfElements = 1000;

// Module pattern to store sensor data
// http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html
var sensorData = (function () {
    var plot;
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
        plot = $.plot("#placeholder", [[0, 0]], {
            yaxis: {
                min: min,
                max: max
            },
            xaxis: {
                show: false,
                min: 0,
                max: maxNumOfElements * updateInterval
            }
        });
    };

    pub.plotData = function() {
        var points = scaleData(data);
        plot.setData([points]);
        plot.draw();
    };

    return pub; // expose externally
}());

function scaleData(data) {
    var res = [];
    var x_min = data[0][0];
    var x_max = data[data.length-1][0];
    var period = (x_max - x_min) / (data.length * updateInterval);
    var res = data.map(function(d, i){
        return [(d[0] - x_min) / period, d[1]]
    });
    return res;
}

function readSensor() {
    $.getJSON('./sensors/dummy', function(data, status) {
    sensorData.addData([$.now(), data.parameter])});
}

function updateGraph() {
    readSensor();
    sensorData.plotData();
}

$( document ).ready(function() {
    $.when( $.getJSON('./sensors/dummy') ).done(function(data, status) {
        sensorData.initPlot(data.minimum, data.maximum);
        setInterval(updateGraph, updateInterval);
    });
});
