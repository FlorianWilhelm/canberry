var sensorData = (function () {
    var data = []; // private
    var pub = {}; // public object - returned at end of module

    pub.addData = function(value) {
        data.push(value);
    };

    pub.clearData = function() {
        data = [];
    };

    pub.getData = function() {
        return data;
    };

    pub.plotData = function() {
        var points = [];
		for (var i = 0; i < data.length; ++i) {
			points.push([i, data[i]])
		}
        $.plot("#placeholder", [points], {
            xaxis: {
			    show: false
			}
		});
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
    setInterval(updateGraph, 1000);
});
