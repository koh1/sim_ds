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



function search_results() {
    var key = $("#results_search_in").val();
    $.ajax({
	async: false,
	type: 'post',
	url: "/search_results/",
	data: {
	    'search_key': key,
	},
	success: function(data) {
	    show_search_results(data);
	}
    });
}

function show_search_results(data) {
    $("#search_results_table").empty();
    str = ""
    for (var i=0; i < data.length; i++) {
	str += "<tr><td id='" + i + "_sim_id'>" + data[i].sim_id + 
	    "</td><td id='" + i + "_db_host'>" + data[i].db_host + 
	    "</td><td id='" + i + "_db_port'>" + data[i].db_port +
	    "</td><td id='" + i + "_db_name'>" + data[i].db_name +
	    "</td><td id='" + i + "_sim_id'>" + data[i].sim_id + 
	    "</td><td>" + 
	    "<button class='btn btn-primary' onclick='location.href=\"/result_viewer/" + data[i].sim_id + "/\"'>View</button>" + 
	    "</td><td></tr>";

//	    "<button class='btn btn-primary' onclick='/analyzer/" + data[i].sim_id + "/'>select</button></td></tr>";
    }
    $("#search_results_table").append(str);
}

