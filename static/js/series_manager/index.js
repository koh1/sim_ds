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
	    "<label for='search_results_select'>Results</label>" +
	    "<select class='form-control' onchange='input_collection_name(this)' id='search_results_select'>" +
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
	    "<button type='submit' class='btn btn-primary'>Submit</button>" +
	    "</form>";
    } else if (e.value == 2) {

    } else if (e.value == 3) {
	
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