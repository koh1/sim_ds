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
    elem_str = "";
    for (var key in localStorage) {
	elem_str += "<tr><td>" + key + "</td>" +
	    "<td>" + localStorage.getItem(key).length + "</td>" + 
	    "<td>" + "<button class='btn btn-primary' onclick='show_series(\"" + key + "\")'>Show</button></td>" +
	    "<td>" + "<button class='btn btn-danger' onclick='delete_series(\"" + key + "\")'>Delete</button></td></tr>";
    }
    $("#series_table_body").empty();
    $("#series_table_body").append(elem_str);
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
	elem_str = "<form role='form'>" +
	    "<div class='form-group'>" +
	    "<label for='series_name'>Name of this Series</label>" + 
	    "<input type='text' class='form-control' id='series_name' placeholder='Input the name of this series.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='search_keyword'>Results Search</label>" + 
	    "<input type='text' onkeyup='search_results()' class='form-control' id='search_keyword' placeholder='Input keyword.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='search_results_select'>Result Candidates</label>" +
	    "<select class='form-control' onclick='input_collection_name(this)' id='search_results_select'>" +
	    "</select>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='collection'>Collection</label>" +
	    "<input type='text' id='collection' class='form-control' placeholder='Input collection name.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='query'>Query</label>" +
	    "<input type='text' id='query' class='form-control' placeholder='Input mongodb query using json.'>" +
	    "</div>" +
	    "<button type='submit' class='btn btn-primary' onclick='make_series_from_mdb()'>Submit</button>" +
	    "</form>";
    } else if (e.value == 2) {
	elem_str = "<div class='form-group'>" +
	    "<label for='series_name'>Name of this Series</label>" + 
	    "<input type='text' class='form-control' id='series_name' placeholder='Input the name of this series.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='local_series_array_json'>Local Series Array (JSON)</label>" + 
	    "<input type='text' class='form-control' id='local_series_array_json' placeholder='Input Array of Local Series with JSON format.'>" +
	    "</div>" +
	    "<button type='submit' onclick='make_series_from_local()' class='btn btn-primary'>Submit</button>";

    } else if (e.value == 3) {
	elem_str = "<div class='form-group'>" +
	    "<label for='series_name'>Name of this Series</label>" + 
	    "<input type='text' class='form-control' id='series_name' placeholder='Input the name of this series.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='raw_json_series'>Raw JSON Series</label>" + 
	    "<input type='text' class='form-control' id='raw_json_series' placeholder='Input Series with JSON format.'>" +
	    "</div>" +
	    "<button type='submit' onclick='make_series_from_raw()' class='btn btn-primary'>Submit</button>";
	
    } else if (e.value == 4) {
	elem_str = "<form role='form' action='make_series_from_mdb()'>" +
	    "<div class='form-group'>" +
	    "<label for='series_name'>Name of this Series</label>" + 
	    "<input type='text' class='form-control' id='series_name' placeholder='Input the name of this series.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='search_keyword'>Results Search</label>" + 
	    "<input type='text' onkeyup='search_results()' class='form-control' id='search_keyword' placeholder='Input keyword.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='search_results_select'>Result Candidates</label>" +
	    "<select class='form-control' onclick='input_collection_name(this)' id='search_results_select'>" +
	    "</select>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='collection'>Collection</label>" +
	    "<input type='text' id='collection' class='form-control' placeholder='Input collection name.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='query'>Query</label>" +
	    "<input type='text' id='query' class='form-control' placeholder='Input mongodb query using json.'>" +
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label>Statistic Functions</label>" +
	    "<div class='radio'>" + 
	    "<label>" +
	    "<input type='radio' name='statistic_funcs' id='statf_1' value='1' checked> Mean" +
	    "</label>" +
	    "</div>" + 
	    "<div class='radio'>" + 
	    "<label>" +
	    "<input type='radio' name='statistic_funcs' id='statf_2' value='2'> Max" +
	    "</label>" +
	    "</div>" + 
	    "<div class='radio'>" + 
	    "<label>" +
	    "<input type='radio' name='statistic_funcs' id='statf_3' value='3'> Min" +
	    "</label>" +
	    "</div>" + 
	    "<div class='radio'>" + 
	    "<label>" +
	    "<input type='radio' name='statistic_funcs' id='statf_4' value='4'> Median" +
	    "</label>" +
	    "</div>" + 
	    "<div class='radio'>" + 
	    "<label>" +
	    "<input type='radio' name='statistic_funcs' id='statf_5' value='5'> Standard Deviation" +
	    "</label>" +
	    "</div>" + 
	    "<div class='radio'>" + 
	    "<label>" +
	    "<input type='radio' name='statistic_funcs' id='statf_6' value='6'> Rolling mean" +
	    "</label>" +
	    "</div>" + 
	    "</div>" +
	    "<div class='form-group'>" +
	    "<label for='query'>Rolling Mean Span</label>" +
	    "<input type='number' id='roll_mean_span' class='form-control'>" +
	    "</div>" +
	    "<button type='submit' class='btn btn-primary'>Submit</button>" +
	    "</form>";
	
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
    
    $("#search_results_select").empty();
    $("#search_results_select").append(opts_str);
}

function input_collection_name(e) {
    $("#collection").val(e.value);
}

function make_series_from_mdb() {
    var series_name = "series_" + $("#series_name").val();
    var query = JSON.parse($("#query"));
    var sim_id = $("#search_results_select").val();
    var coll = $("#collection").val();
    data = {
	"sim_id": sim_id,
	"collection_name": coll,
	"query": query
    };
    alert(data);
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