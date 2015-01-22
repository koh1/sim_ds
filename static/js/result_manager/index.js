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
	    "</td><td id='" + i + "_queue_method'>" + data[i].queue_method + 
	    "</td><td id='" + i + "_num_of_users'>" + data[i].num_of_users +
	    "</td><td id='" + i + "_contents_size'>" + data[i].contents_size +
	    "</td><td id='" + i + "_planning_cycle'>" + data[i].planning_cycle + 
	    "</td><td id='" + i + "_user_act_span'>" + data[i].user_act_span + 
	    "</td><td id='" + i + "_scale'>" + data[i].scale + 
	    "</td><td id='" + i + "_num_of_areas'>" + data[i].num_of_areas + 
	    "</td><td id='" + i + "_owner'>" + data[i].owner + 
	    "</td><td id='" + i + "_status'>" + data[i].status + 
	    "</td><td id='" + i + "_progress'>" + data[i].progress + 
	    "</td><td><button class='btn btn-primary' onclick='location.href=\"/view_detail/" + data[i].id + "/\"'>View</button>" + 
	    "</td><td><button class='btn btn-danger' onclick='location.href=\"/delete_sim_result/" + data[i].id + "\"'>Delete</button>" +
	    "</td></tr>";
    }
    $("#search_results_table").append(str);
}


