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
        plot = $.plot("#placeholder", [[0, 0]], {
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

function readSensor() {
    return $.getJSON('./sensors/dummy', function(data, status) {
    sensorData.addData([$.now(), data.parameter])});
}

function updateGraph() {
    $.when( readSensor() ).done(sensorData.plotData);
}

$( document ).ready(function() {
    $.when( readSensor() ).done(function(data, status) {
        sensorData.initPlot(data.minimum, data.maximum);
        setInterval(updateGraph, updateInterval);
    });
});
