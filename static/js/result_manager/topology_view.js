

function get_topology_data_proto(scale, area) {
    file_name = "/static/data/topo_d3_%d_area%d.json" % (scale, area)
    $.ajax({
	async: 'false',
	type: 'GET',
	url: file_name,
	dataType: 'json',
	success: function(data) {
	    make_topology_proto(data);
	}
    });
}
function make_topology_proto(data) {
    var svg = d3.select("#topology_svg").append("svg")
	.attr({
	    "width": 800,
	    "height": 400
	});
    var zoom = d3.behavior.zoom()
	.scaleExtent([1,10])
	.on("zoom", zoomed);
    
    var container = svg.append("g")
	.call(zoom);
    var tree = d3.layout.tree().size([800,380]);
    var nodes = tree.nodes(data);

    container.selectAll("path")
	.data(tree.links(nodes))
	.enter()
	.append("path")
	.attr("d", d3.svg.diagonal())
	.attr("fill", "none")
	.attr("stroke", "#aa2222")
	.attr("stroke-width", 1)
	.attr("transform", "translate(0, " + 10 + ")");

    container.selectAll("circle")
	.data(nodes)
	.enter()
	.append("circle")
	.on("click", function(d) {
	    alert(d["name"]);
	})
	.attr("cx", function(d){return d.x})
	.attr("cy", function(d){return d.y + 10})
	.attr("r", 5)
	.style("stroke", "white")
	.style("fill", "#aa2222");

    function zoomed() {
	container.attr("transform",
		       "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }
}


