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
    var text = "";
    for (var k in data) {
	text += k + ": " + data[k] + "\n";
    }
    $("#console").val(text);
}

