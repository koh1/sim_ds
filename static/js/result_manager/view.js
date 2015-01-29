function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
	    var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
	    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
	    }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


var console_arry;
var chart_svg;
var topology_svg;
var tree, nodes;
$(function() {
    if (localStorage.getItem("console_log") == null) {
	localStorage.setItem("console_log", JSON.stringify([]));
    }
    console_arry = JSON.parse(localStorage.getItem("console_log"));
    $("#console").val(console_arry.join('\n'));
    
    chart_svg = d3.select("#chart_place").append("svg")
	.attr({
	    "width": 800,
	    "height": 400
	});
    topology_svg = d3.select("#topology_svg").append("svg")
	.attr({
	    "width": 1024,
	    "height": 600
	});
});


function update_columns(pkid) {
    var c_name = $("#collection").val();
    var url = "/view/get_collection_columns/" + pkid + "/" + c_name + "/";
    $.ajax({
	async: false,
	type: 'get',
	url: url,
	success: function(data) {
	    update_columns_view(data);
	}
    });
}
function update_columns_view(data) {
    var html = "";
    var time_exists = false;
    for (var k in data) {
	html += "<option value='" + k + "'>" + k + "</option>";
	if (k == 'time') {
	    time_exists = true;
	}
    }
    $("#columns").html(html);
    if (time_exists) {
	$("#time_chart_btn").attr("disabled", false);
    } else {
	$("#time_chart_btn").attr("disabled", true);
    }
}

function get_statistics(pkid) {
    var c_name = $("#collection").val();    
    var col = $("#columns").val();
    var url = "/view/get_statistics/" + pkid + "/" + c_name + "/" + col + "/";
    $.ajax({
	async: false,
	type: 'get',
	url: url,
	success: function(data) {
	    get_statistics_view(data);
	}
    });
}
function get_statistics_view(data) {
    console_log(JSON.stringify(data));
}

function console_log(str) {
    if (console_arry.length  > 19) {
	console_arry.shift();
    }
    console_arry.push(str);
    localStorage.setItem("console_log", JSON.stringify(console_arry));
    $("#console").val(console_arry.join('\n'));
}

function clear_console() {
    console_arry = []
    $("#console").val(console_arry.join('\n'));
    localStorage.setItem("console_log", JSON.stringify([]));
}

function get_topology_data(pkid) {
}

function make_system_topology(pkid,scale,num_of_areas) {
    var url = "/static/data/topo_" + scale + "_area" + num_of_areas + ".json";
    $.ajax({
	async: false,
	type: 'get',
	url: url,
	success: function(data) {
	    make_system_topology_view(data);
	}
    });
}
function make_system_topology_view(data) {
    tree = d3.layout.tree().size([1024,500]);
    nodes = tree.nodes(data);

    topology_svg.selectAll("path")
	.data(tree.links(nodes))
	.enter()
	.append("path")
	.attr("d", d3.svg.diagonal())
	.attr("fill", "none")
	.attr("stroke", "#337ab7")
	.attr("stroke-width", 1)
	.attr("transform", "translate(0, " + 10 + ")");
    topology_svg.selectAll("circle")
	.data(nodes)
	.enter()
	.append("circle")
	.attr("cx", function(d){return d.x})
	.attr("cy", function(d){return d.y + 10})
	.attr("r", 5)
	.style("stroke", "#eee")
	.style("fill", "#337ab7");
}