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


function show_nwk_chart() {
    var urlstr = "/analyzer/analyze/get_nwk_chart_data/";
    $.ajax({
	async: false,
	type: 'post',
	
	url: urlstr,
	data: {
	    'x': 'time',
	    'y': 'nw_usage',
	    'nwk_name': 'edge_nwk'
	},
	success: function(data) {
	    draw_nwk_chart(data);
	}
    });
}

function draw_nwk_chart(data) {
    alert(data);
//    var chart = c3.generate({
//	bindto: '#nwk_chart',
//	data: {
//            columns: data
//	}
//    });
}

function add_series() {
    
}