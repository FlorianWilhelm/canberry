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

    pub.plotData = function() {
        if (! plot) {
            plot = $.plot("#placeholder", [], {
                xaxis: {
                    show: false,
                    min: 0,
                    max: maxNumOfElements
                }
            });
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

function updateGraph() {
    $.get('./sensors/dummy', function(data, status) {
        data = JSON.parse(data);
        sensorData.addData(data.parameter)});
    sensorData.plotData();
    }

$( document ).ready(function() {
    setInterval(updateGraph, 100);
});
