"use strict";

var updateInterval = 100;

var sensorData = (function () {
    var maxNumOfElements = 1000;
    var plot;
    var data = []; // private
    var pub = {}; // public object - returned at end of module

    pub.addData = function(value) {
        if (data.length > maxNumOfElements) {
            data.shift();
        }
        data.push(value);
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
                max: maxNumOfElements
            }
        });
    };

    pub.plotData = function() {
        if (! plot) {

        }
        var points = [];
		for (var i = 0; i < data.length; ++i) {
			points.push([i, data[i]]);
		}
        plot.setData([points]);
        plot.draw();
    };

    return pub; // expose externally
}());

function readSensor() {
    $.getJSON('./sensors/dummy', function(data, status) {
    sensorData.addData(data.parameter)});
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
