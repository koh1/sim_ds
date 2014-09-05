
function make_series_add_form(e) {
    var elem_str = "";
    if (e.value == 1) {
	elem_str = "<form role='form'>" +
	    "<div class='form-group'>" +
	    "<label for='exampleInputEmail1'>Email address</label>" + 
	    "<input type='email' class="form-control" id="exampleInputEmail1" placeholder="Enter email">
  </div>
  <div class="form-group">
    <label for="exampleInputPassword1">Password</label>
    <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
  </div>
  <div class="form-group">
    <label for="exampleInputFile">File input</label>
    <input type="file" id="exampleInputFile">
    <p class="help-block">Example block-level help text here.</p>
  </div>
  <div class="checkbox">
    <label>
      <input type="checkbox"> Check me out
    </label>
  </div>
  <button type="submit" class="btn btn-default">Submit</button>
</form>
";
    } else if (e.value == 2) {

    } else if (e.value == 3) {
	
    }
    $("#series_add_form").clear();
    $("#series_add_form").append(elem_str);
    
}