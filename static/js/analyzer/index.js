var loaded_dfs = {};

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


function draw_chart(data) {
    var xkey = "";
    var valx = [];
    var data = [];
    for (var k in loaded_dfs) {
	if (loaded_dfs[k]['xaxis'] == true) {
	    xkey = k;
	    valx = [k].concat(loaded_dfs[k]['value']);
	} else {
	    var oney = [k].concat(loaded_dfs[k]['value']);
	    data.push(oney);
	}
	loaded_dfs[k]['label'] = $("#lable_" + k).val();
    }
    if (xkey == "") {
	alert("Please specify a series for x-axis.");
	return;
    }
    data.push(valx);
    var chart = c3.generate({
	bindto: '#chart',
	data: {
	    x: xkey,
	    columns: data,
	    type: 'scatter'
	},

	axis: {
	    x: {
		label: 'time',
		tick: {
		    fit: true
		}
	    },
	    y: {
		label: 'traffic'
	    }
	}
    });
}


function get_df_sample(id) {
    var urlstr = "/analyzer/get_df_sample/";
    $.ajax({
	async: false,
	type: 'post',
	url: urlstr,
	data: {
	    'id': id
	},
	success: function(data) {
	    show_df_sample(data);
	},
    });
}

function show_df_sample(data) {
    str = ""
    for (var k in data) {
	str += k + ": " + data[k] + "\n";
    }
    alert(str);
}

function make_series_for_chart(dfdid) {
    var select_item_id = "#selected_item_" + dfdid;
    data = {
	'id': dfdid,
	'column_name': $(select_item_id).val()
    };
    var urlstr = "/series_manager/get_series_from_dfd/";
    $.ajax({
	async: false,
	type: 'post',
	dataType: 'json',
	data: data,
	url: urlstr,
	success: function(data) {
	    store_series_for_chart(data);
	},
    });
}
function store_series_for_chart(data) {
    loaded_dfs[data['key']] = {
	'label': data['key'],
	'value': data['value'],
	'xaxis': false
    };
    var elstr = "<tr>";
    elstr += "<td><a href='#' onclick='show_series(\"" + data['key'] + "\")'>" + data['key'] + "</a></td>"; 
    elstr += "<td>";
    elstr += "<input type='text' id='label_" + data['key'] + "' class='form-control' value='" + data['key'] + "'></td>";
    elstr += "<td><div class='radio'><label><input type='radio' name='xaxis' value='" + data['key'] + "' onclick='check_as_xaxis(this)'>select as x-axis</label></div></td>";
    elstr += "</tr>";
    $("#selected_data_frames").append(elstr);
}

function check_as_xaxis(el) {
    for (var k in loaded_dfs) {
	loaded_dfs[k]['xaxis'] = false;
    }
    loaded_dfs[el.value]['xaxis'] = true;
}


function show_series(key) {
    alert(loaded_dfs[key]['value']);
}

