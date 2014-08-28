var paper;
var nodes;
var paths;
var texts;
var bubbles;
var style;

var width = 1200;
var height = 400;

var colors = {
    'gray-darker': "#222",
    'gray-dark': "#333",
    'gray': "#555",
    'gray-light': "#999",
    'gray-lighter': "#eee",
    'bs-primary': "#428bca",
    'bs-success': "#5cb85c",
    'bs-info': "#5bc0de",
    'bs-warning': "#f0ad4e",
    'bs-danger': "#d9534f"
};

var nodes_per_layer;
var span_nodes;
var vert_span_nodes;

var traffic_avg;
var traffic_text;
var db_name;
var coll;
var start_time;
var step_width;


$(function() {
    paper = Raphael("canvas", width, height);
    nodes = {};
    paths = {};
    texts = {};
    bubbles = {};
    traffic_avg = {};
    traffic_text = {};
    $.ajax({
	type: 'GET',
	url: '/static/data/topo2.json',
	dataType: 'json',
	success: function(data) {
	    make_topology(data);
	}
    });
});



function make_topology(data) {
    
    // serch root and inspect depth
    var max_layer = 0;

    for (var key in data) {
	if (data[key]['layer'] > max_layer) {
	    max_layer = data[key]['layer'];
	}
    }
    
    // nodes
    nodes_per_layer = new Array(max_layer+1);
    for (var i = 0; i < nodes_per_layer.length; i++) {
	nodes_per_layer[i] = [];
    }
    for (var key in data) {
	nodes_per_layer[data[key]['layer']].push(data[key]);
    }
    
    span_nodes = new Array(max_layer+1);
    for (var i = 0; i < span_nodes.length; i++) {
	span_nodes[i] = width / (nodes_per_layer[i].length + 1);
    }
    vert_span_nodes = height / (max_layer + 2);
    
    // place root node
    var root_nx = span_nodes[0] * 1;
    var root_ny = vert_span_nodes / 2;
    nodes[nodes_per_layer[0][0]['name']] = paper.rect(root_nx, root_ny, 
						      20,20,1).attr({
							  'fill': colors['gray-light'],
							  'stroke': colors['gray-light'],
							  'stroke-width': 0.5
						      });
    texts[nodes_per_layer[0][0]['name']] = paper.text(
	get_node_center(nodes[nodes_per_layer[0][0]['name']])[0],
	get_node_center(nodes[nodes_per_layer[0][0]['name']])[1],
	nodes_per_layer[0][0]['name']).rotate(90);
    // place layer 1 nodes
    for (var i=0; i < nodes_per_layer[1].length; i++) {
	var nd = nodes_per_layer[1][i];
	var nx = span_nodes[1] * (i+1);
	var ny = vert_span_nodes/2 + vert_span_nodes * 1;
	nodes[nd['name']] = paper.rect(nx, ny,
				       20,
				       20,1).attr({
					   'fill': colors['gray-light'],
					   'stroke': colors['gray-light'],
					   'stroke-width': 0.5
				       });
	texts[nd['name']] = paper.text(
	    get_node_center(nodes[nd['name']])[0],
	    get_node_center(nodes[nd['name']])[1],
	    nd['name']).rotate(90);
	
	if (nd['parent'] != "") {
	    path_name = nd['paernt'] + "_" + nd['name'];
	    path_str = "M" + get_node_center_str(nodes[nd['parent']]) +
		"L" + get_node_center_str(nodes[nd['name']]);
	    paths[path_name] = paper.path(path_str).attr({
		'stroke': colors['gray']
	    });
	}
    }
    for (var i=0; i < nodes_per_layer[2].length; i++) {
	var nd = nodes_per_layer[2][i];
	var nx = span_nodes[2] * (i+1) - 10;
	var ny = vert_span_nodes/2 + vert_span_nodes * 2;
	nodes[nd['name']] = paper.rect(nx, ny,
				       20,
				       20,1).attr({
					   'fill': colors['gray-light'],
					   'stroke': colors['gray-light'],
					   'stroke-width': 0.5
				       });
	texts[nd['name']] = paper.text(
	    get_node_center(nodes[nd['name']])[0],
	    get_node_center(nodes[nd['name']])[1],
	    nd['name']).attr({'text-size': 6}).rotate(90);

	path_name = nd['paernt'] + "_" + nd['name'];
	path_str = "M" + get_node_center_str(nodes[nd['parent']]) +
	    "L" + get_node_center_str(nodes[nd['name']]);
	paths[path_name] = paper.path(path_str).attr({
	    'stroke': colors['gray']
	});
	make_subtree(data, nodes[nd['name']], nd['name']);
    }
    for (var key in nodes) {
	nodes[key].toFront();
    }
    for (var key in texts) {
	texts[key].toFront();
    }
}

function sleep(time, callback, param) {
    setTimeout(callback, time, param);
}

function show_traffic() {
    traffic_avg = {};
    db_name = $("#db_name").val();
    coll = $("#db_coll").val();
    start_time = parseInt($("#start_time").val());
    step_width = parseInt($("#step_width").val());
    if (db_name == "" || coll == "") {
	alert('Input DB name and Collection Name');
	return;
    }
    for (var key in texts) {
	texts[key].hide();
    }
    for (var i = 0; i < parseInt($("#num_of_steps").val()); i++) {
	sleep(100, show_traffic_each, i);
    }
    /*
    for (var key in texts) {
	texts[key].show();
	texts[key].toFront();
    }
    */
    $("#show_avg_btn").attr('disabled', false);
}

function show_avg_traffic() {
    for (var key in traffic_avg) {
	var step_width_ms = parseInt($("#step_width").val());
	var num_of_steps = parseInt($("#num_of_steps").val());
	var span_sec = step_width_ms * num_of_steps / 1000;
	var avg = traffic_avg[key] / span_sec / 1000000.0; // Gbit
	if (avg < 1) {
	    avg = 0.0;
	}
//	avg_split = avg.toString().split(".");
//	avg_str = avg_split[0] + avg_split[1].substring(0,2);
	traffic_text[key] = paper.text(
	    get_node_center(nodes[key])[0],
	    get_node_center(nodes[key])[1],
	    avg.toString().substring(0,7)).attr({'text-size': 4}).rotate(90);
	bubbles[key].attr({
	    r: traffic_avg[key]*1e-10
	});
    }
}

function show_traffic_each(i) {
    var t = i * step_width + start_time;
    var urlstr = "get_nwk_traffic/" + db_name + "/" + coll + "/" + t + "/";
    $.ajax({
	async: false,
	type: 'GET',
	url: urlstr,
	dataType: 'json',
	success: function(data) {
	    draw_bubble(data);
	}
    });
}


function draw_bubble(data) {
    for (var i=0; i < data.length; i++ ) {
	nd_name = data[i]['nwk_name'];
	nd = nodes[nd_name];
	if (bubbles[nd_name] == null) {
	    bubbles[nd_name] = paper.circle(get_node_center(nd)[0],
					    get_node_center(nd)[1],
					    data[i]['nw_usage_bits'] * 1e-7).attr({
						'fill': colors['bs-primary'],
						'fill-opacity': 0.8,
						'stroke': colors['bs-primary']
					    });
	    traffic_avg[nd_name] = data[i]['nw_usage_bits'];
	} else {
	    bubbles[nd_name].attr({r: data[i]['nw_usage_bits']*1e-7});
//	    traffic_avg[nd_name] = (traffic_avg[nd_name] + data[i]['nw_usage_bits'])/2;
	    traffic_avg[nd_name] += data[i]['nw_usage_bits'];
	}
    }
}

function make_subtree(data, p_node, p_name) {
    var p_layer = data[p_name]['layer'];
    for (var i = 0; i < data[p_name]['children'].length; i++) {
	var nd_name = data[p_name]['children'][i];
	var nx = p_node.attr().x - span_nodes[p_layer]/2 + 
	    span_nodes[p_layer + 1] * (i+1);
	var ny = vert_span_nodes/2 + vert_span_nodes * (p_layer + 1);
	nodes[nd_name] = paper.rect(nx, ny,
				    span_nodes[p_layer+1]/2,
				    span_nodes[p_layer+1]/2,1).attr({
					'fill': colors['gray-light'],
					'stroke': colors['gray-light'],
					'stroke-width': 0.5
				    });
	texts[nd_name] = paper.text(
	    get_node_center(nodes[nd_name])[0],
	    get_node_center(nodes[nd_name])[1],
	    nd_name).attr({'text-size': 6}).rotate(90);

	path_name = p_name + "_" + nd_name;
	path_str = "M" + get_node_center_str(nodes[p_name]) +
	    "L" + get_node_center_str(nodes[nd_name]);
	paths[path_name] = paper.path(path_str).attr({
	    'stroke': colors['gray']
	});
	make_subtree(data, nodes[nd_name], nd_name);
    }
}

function load_sim_params() {
    
}

function get_node_center(node) {
    var x = node.attr().x
    var y = node.attr().y
    
    var width = node.attr().width
    var height = node.attr().height
    
    return [x + width/2, y + height/2]
    
}

function get_node_center_str(node) {
    center = get_node_center(node)

    return "" + center[0] + "," + center[1]
}

function cprintf(fmt, params) {
    return fmt.replace(/%{(.*?)}/g, function($0, $1) {
	return ( params[$1] && typeof(params[$1]) != "object" ) ?
	    params[$1].toString() : JSON.stringify(params[$1]);
    });
}
