$(function(){
	console.log("loas");

	$("#earlierButton").click(function() {
		navigate(this);
	});
	$("#laterButton").click(function() {
		navigate(this);
	});

	function navigate(button)
	{
		console.log("lo");
		console.log($(button));
		var page = $(button).attr("page");
		var link = collectFilters() + "?page="+page;
		console.log(link);
		$(button).prop("href", link);
	}
	function collectFilters() {
		return "/submissions";
	}
});