$(function(){

	$(".group-selector").click(function() {
		var group = "." + $(this).attr("group");
		console.log(group);
		$(".all").hide();
		$(group).show();
		$(group).each(function(i, elem) {
			$(elem).children("td:first").html(i+1);
		});
	});
	
});