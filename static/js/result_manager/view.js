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
    
    var tree = d3.layout.tree().size([800,380]);
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
	.on("click", function(d) {
	    alert(d["name"]);
	})
	.attr("cx", function(d){return d.x})
	.attr("cy", function(d){return d.y + 10})
	.attr("r", 5)
	.style("stroke", "white")
	.style("fill", "#aa2222");
}



window.onload = function() {
    var svgWidth = 320;
    var svgHeight = 240;
    var offsetY = 10;
    var svg = d3.select("body").append("svg")
	.attr({
	    "width":svgWidth,
	    "height": svgHeight
	});

    var circles = svg.selectAll("circle")
	.data([10, 12, 14])
	.enter()
	.append("circle");

    circles.style("fill", "steelblue");
    circles.attr("stroke", "white");
    circles.attr("cx", function(d, i) {return (i*50) + 25});
    circles.attr("cy", 90);
    circles.attr("r",function(d) {return d});
    
    
    

    var rects = svg.selectAll("rest")
	.data([10,20,15,30,22])
	.enter()
	.append("rect");

    rects.style("fill", "#aa2222");
    rects.attr("stroke", "white");
    rects.attr("x", function(d, i) {return (i*50)+50});
    rects.attr("y", 120);
    rects.attr("width", function(d) {return d});
    rects.attr("height", function(d) {return d});
    rects.on("click", function(d) { 
	alert(d);
    });

};

var data = {
    name:"root",
    children:[
	{name: "n11"},
	{name: "n12"},
	{name: "n13",
	 children: [
	     {name: "n131"},
	     {name: "n132"},
	     {name: "n133"},
	 ]
	},
	{name: "n14",
	 children: [
	     {name: "n141"},
	     {name: "n142"},
	     {name: "n143"},
	     {name: "n144"},
	 ]
	},
    ]
}

    var svgWidth = 320;
    var svgHeight = 240;
    var offsetY = 10;
    var svg = d3.select("#system_view").append("svg")
	.attr({
	    "width":svgWidth,
	    "height": svgHeight
	});

var tree = d3.layout.tree().size([320,220]);

var nodes = tree.nodes(data);

svg.selectAll("path")
    .data(tree.links(nodes))
    .enter()
    .append("path")
    .attr("d", d3.svg.diagonal())
    .attr("fill", "none")
    .attr("stroke", "#ff9999")
    .attr("stroke-width", 1)
    .attr("transform", "translate(0, " + offsetY + ")");

svg.selectAll("circle")
    .data(nodes)
    .enter()
    .append("circle")
    .on("click", function(d) {
	alert(d["name"]);
    })
    .attr("cx", function(d){return d.x})
    .attr("cy", function(d){return d.y + offsetY})
    .attr("r", 5)
    .style("stroke", "white")
    .style("fill", "#ff9999");

