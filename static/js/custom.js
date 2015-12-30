var last_loaded = 0;
var track_row = '<div class="row"><div class="grid-25" style="margin-right: 5px; height: 150px; width: 150px; background-size: 100%;background-image: url({image});"><a href="http://soundcloud.com/{track-target-permalink}"><span class="sc-style">{track-target-permalink}\'s like</span></a></div><iframe class="grid-75" height="150" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{track-sc_id}&amp;auto_play=false&amp;hide_related=true&amp;show_comments=false&amp;show_user=true&amp;show_reposts=false&amp;visual=true"></iframe></div><br>';

function get_more() {
  $.getJSON($SCRIPT_ROOT + '/_more', {
    start: last_loaded,
    end: last_loaded + 5
  }, function(data) {
    var tracks = [];
    $.each( data.tracks, function( i, item ) {
      tracks.push(track_row.replace('{track-sc_id}', item.sc_id).
                  replace('{track-target-permalink}', item.target_permalink).
                  replace('{track-target-permalink}', item.target_permalink).
                  replace('{image}', data.images[item.target_id])
                  );
    });
    $('#tracks').append(tracks.join(''));
  });
  last_loaded += 5;
  return false; 
}


$(function() {
  get_more();
	$('#load-more').click( function() {
    get_more();
  });
});