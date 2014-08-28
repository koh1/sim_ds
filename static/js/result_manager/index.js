

function search_results() {
    var key = $("#results_search_in").val();
    $.ajax({
	async: false,
	type: 'post',
	url: "search_result",
	data: {
	    'key': key
	},
	success: function(data) {
	    show_search_results(data);
	}
    });
}

function show_search_results(data) {
    

}