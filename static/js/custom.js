$(function() {
	$('a#get').bind('click', function() {
  		$.getJSON($SCRIPT_ROOT + '/_more', {
    		start: $('input[name="begin"]').val(),
    		end: $('input[name="end"]').val()
  		}, function(data) {
    		$("#result").append($('<li>').text(JSON.stringify(data.tracks)));
  		});
  		return true;
	});
});