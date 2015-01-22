$(function() {
    if (window.File && window.FileReader && window.FileList && window.Blob) {
    } else {
	alert('The File APIs are NOT fully SUPPORTED with this browser.');
    }
});


function config_file_selected() {
    var selectedFile = document.getElementById("bconffile").files[0];
    var reader = new FileReader();
    reader.addEventListener('load', function(e) {
	var config = jsyaml.load(reader.result);
	var htmlstr = "";
	for (var k in config) {
	    htmlstr += "<tr><td>" + k + "</td><td>" + jsyaml.dump(config[k]) + "</td></tr>";
	}
	$("#configurations").html(htmlstr);
    });
    reader.readAsText(selectedFile);
    
    get_topology_data_proto();
}


function get_topology_data_proto() {
    $.ajax({
	async: 'false',
	type: 'GET',
	url: '/static/data/topo_d3.json',
	dataType: 'json',
	success: function(data) {
	    make_topology_proto(data);
	}
    });
}

function make_topology_proto(data) {
    var svg = d3.select("#topology_svg").append("svg")
	.attr({
	    "width": 600,
	    "height": 400
	});
    
    var tree = d3.layout.tree().size([600,380]);
    var nodes = tree.nodes(data);

    svg.selectAll("path")
	.data(tree.links(nodes))
	.enter()
	.append("path")
	.attr("d", d3.svg.diagonal())
	.attr("fill", "none")
	.attr("stroke", "#aa2222")
	.attr("stroke-width", 1)
	.attr("transform", "translate(0, " + 10 + ")");

    svg.selectAll("circle")
	.data(nodes)
	.enter()
	.append("circle")
	.attr("cx", function(d){return d.x})
	.attr("cy", function(d){return d.y + 10})
	.attr("r", 5)
	.style("stroke", "white")
	.style("fill", "#aa2222");
}