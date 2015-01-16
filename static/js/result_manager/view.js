$(function() {

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
    var svg = d3.selectAll("body").append("svg")
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
    .attr("stroke", "#aaa")
    .attr("stroke-width", 1)
    .attr("transform", "translate(0, " + offsetY + ")");

svg.selectAll("circle")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("cx", function(d){return d.x})
    .attr("cy", function(d){return d.y + offsetY})
    .attr("r", 5)
    .style("stroke", "#")
    .style("fill", "white");

});