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

$(function() {
/*
    elem_str = "";
    for (var key in localStorage) {
	elem_str += "<tr><td>" + key + "</td>" +
	    "<td>" + localStorage.getItem(key).length + "</td>" + 
	    "<td>" + "<button class='btn btn-primary' onclick='show_series(\"" + key + "\")'>Show</button></td>" +
	    "<td>" + "<button class='btn btn-danger' onclick='delete_series(\"" + key + "\")'>Delete</button></td></tr>";
    }
    $("#series_table_body").empty();
    $("#series_table_body").append(elem_str);
*/
});

function delete_series(k) {
    localStorage.removeItem(k);
}
function show_series(k) {
    alert(localStorage.getItem(k));
}

function make_series_add_form(e) {
    var elem_str = "";
    if (e.value == 1) {
	elem_str = "<div class='form-group'>" +
	    "<label for='series_name'>Name of this Series</label>" +
	    "<input type='text' class='form-control' id='series_name' placeholder='Input the name of this series.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='search_keyword'>Results Search</label>" + 
	    "<input type='text' onkeyup='search_results()' class='form-control' id='search_keyword' placeholder='Input keyword.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='sim_id'>Result Candidates</label>" +
	    "<select class='form-control' onclick='input_collection_name(this)' id='sim_id'>" +
	    "</select>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='collection_name'>Collection</label>" +
	    "<input type='text' id='collection_name' class='form-control' placeholder='Input collection name.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='query'>Query</label>" +
	    "<input type='text' id='query' class='form-control' placeholder='Input mongodb query with json format.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='column_items'>Column Items</label>" +
	    "<input type='text' id='column_items' class='form-control' placeholder='Input column items with json array format.'>" +
	    "</div>" + 
	    "<button onclick='make_df_from_mdb()' class='btn btn-primary'>Submit</button>";


    } else if (e.value == 2) {
	elem_str = "<div class='form-group'>" +
	    "<label for='series_name'>Name of this Series</label>" +
	    "<input type='text' class='form-control' id='series_name' placeholder='Input the name of this series.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='local_series_array_json'>How to make Data Frame (JSON)</label>" + 
	    "<input type='text' class='form-control' id='how_to_make_df_json' placeholder='Input Array of Items with JSON format.'>" +
	    "</div>" + 
	    "<button onclick='make_df_from_dfs()' class='btn btn-primary'>Submit</button>";


    } else if (e.value == 3) {
	elem_str = "<div class='form-group'>" +
	    "<label for='series_name'>Name of this Series</label>" +
	    "<input type='text' class='form-control' id='series_name' placeholder='Input the name of this series.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='raw_json_series'>Raw JSON Series</label>" + 
	    "<input type='text' class='form-control' id='raw_df' placeholder='Input Data Frame with JSON format.'>" +
	    "</div>" + 
	    "<button onclick='make_df_from_raw()' class='btn btn-primary'>Submit</button>";

	
    } else if (e.value == 4) {
	elem_str = "<div class='form-group'>" +
	    "<label for='series_name'>Name of this Series</label>" +
	    "<input type='text' class='form-control' id='series_name' placeholder='Input the name of this series.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='search_keyword'>Results Search</label>" + 
	    "<input type='text' onkeyup='search_results()' class='form-control' id='search_keyword' placeholder='Input keyword.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='sim_id'>Result Candidates</label>" +
	    "<select class='form-control' onclick='input_collection_name(this)' id='sim_id'>" +
	    "</select>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='collection_name'>Collection</label>" +
	    "<input type='text' id='collection_name' class='form-control' placeholder='Input collection name.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='query'>Query</label>" +
	    "<input type='text' id='query' class='form-control' placeholder='Input mongodb query using json.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='target_item'>Target Item</label>" +
	    "<input type='text' id='target_item' class='form-control' placeholder='Input target column name.'>" +
	    "</div>" + 
	    "<button onclick='make_df_from_mdb_ws()' class='btn btn-primary'>Submit</button>";

    }
    $("#series_add_form").empty();
    $("#series_add_form").append(elem_str);
}


function search_results() {
    var key = $("#search_keyword").val();
    $.ajax({
	async: false,
	type: 'post',
	url: "/search_results/",
	data: {
	    'search_key': key,
	},
	success: function(data) {
	    make_select_options(data);
	}
    });
}
function make_select_options(data) {
    var opts_str = "";

    for (var i=0; i < data.length; i++) {
	opts_str += "<option value='" + data[i].sim_id + "'>" + data[i].sim_id + "</option>";
    }
    
    $("#sim_id").empty();
    $("#sim_id").append(opts_str);
}

function input_collection_name(e) {
    $("#collection_name").val(e.value);
}

function make_df_from_mdb() {
    var series_name = $("#series_name").val();
    var query = JSON.parse($("#query").val());
    var sim_id = $("#sim_id").val();
    var coll = $("#collection_name").val();
    var column_items = JSON.parse($("#column_items").val());
    data = {
	"series_name": series_name,
	"sim_id": sim_id,
	"collection_name": coll,
	"column_items": JSON.stringify(column_items),
	"query": JSON.stringify(query)
    };
    $.ajax({
	async: false,
	type: 'post',
	dataType: 'json',
	url: "/series_manager/make_df_from_mdb/",
	data: data,
	success: function(data) {
	    make_alert(data);
	}
    });
}

function make_alert(data) {
    $("#alert_region").empty();
    var alert_str = "<div class='alert alert-info alert-dismissible' role='alert'>" +
	"<button type='button' class='close' data-dismiss='alert'>" +
	"<span aria-hidden='true'>&times;</span><span class='sr-only'>Close</span></button>";
    alert_str += "[" + data['status'] + "]" + data["message"];
    alert_str += "</div>";
    $("#alert_region").append(alert_str);

    
}

function make_series_from_json(data) {
    localStorage.setItem(data['series_name'], JSON.stringify(data['series']));
}


function make_series_from_raw() {
    var series_name = "series_" + $("#series_name").val();
    var json_series = JSON.parse($("#raw_json_series").val());
    localStorage.setItem(series_name, JSON.stringify(json_series));
}

function make_series_from_local() {
    var series_name = "series_" + $("#series_name").val();
    var series_arry = JSON.parse($("#local_series_array_json").val());
    var result = [];
    for (var i=0; i < series_arry.length; i++)  {
	var series = JSON.parse(localStorage[series_arry[i]]);
	if (series instanceof Array) {
	    Array.prototype.push.apply(result, series);
	} else {
	    result.push(series);
	}
    }
    localStorage.setItem(series_name, JSON.stringify(result));
}