var sensorData = (function () {
    var data = []; // private
    var pub = {};// public object - returned at end of module

    pub.addData = function(value) {
        data.push(value);
    };

    pub.clearData = function() {
        data = []
    };

    pub.getData = function() {
        return data;
    }

    return pub; // expose externally
}());


function plotSensorData() {

		var d1 = [];
		for (var i = 0; i < 14; i += 0.5) {
			d1.push([i, Math.sin(i)]);
		}

		var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];

		// A null signifies separate line segments

		var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];

		$.plot("#placeholder", [ d1, d2, d3 ]);

		// Add the Flot version string to the footer

		$("#footer").prepend("Flot " + $.plot.version + " &ndash; ");
	}
