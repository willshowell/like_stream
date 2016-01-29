var totalLoaded = 0;
var track_row = '<div class="row"><div class="grid-25 track" style="margin-right: 5px; height: 150px; width: 150px; background-size: 100%;background-image: url({image});"><a href="http://soundcloud.com/{track-target-permalink}"><span class="sc-style">{track-target-permalink}\'s like</span></a></div><iframe class="grid-75" height="150" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{track-sc_id}&amp;auto_play=false&amp;hide_related=true&amp;show_comments=false&amp;show_user=true&amp;show_reposts=false&amp;visual=true"></iframe></div><br>';
var count = 5;

var widgetFrameTemplate = '<iframe class="grid-75 track" id="{frame-id}" src="{widget-source}" frameborder="no" scrolling="no" ></iframe>';
var widgetSource = "https://w.soundcloud.com/player/?url=https://api.soundcloud.com/tracks/{track-sc_id}";
var urlOptions = "&amp;auto_play=false&amp;hide_related=true&amp;show_comments=false&amp;show_user=true&amp;show_reposts=false&amp;visual=true";

/*
<iframe class="grid-75" height="150" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{track-sc_id}&amp;auto_play=false&amp;hide_related=true&amp;show_comments=false&amp;show_user=true&amp;show_reposts=false&amp;visual=true">
<iframe id="sc-widget" src="https://w.soundcloud.com/player/?url=http://api.soundcloud.com/users/1539950/favorites" width="100%" height="465" scrolling="no" frameborder="no"></iframe>
*/

/* Sends AJAX request */
function getMore(loadCount, callback) {
  $.getJSON($SCRIPT_ROOT + '/_more', {
    start: totalLoaded,
    end: totalLoaded + loadCount
  }, function(data) {
    
    if (data.tracks.length == 0) {
      $('#end-stream').show();
    }
    
    /* Iterate through the AJAX return */
    $.each( data.tracks, function( i, item ) {
      
      /* Create widget iFrame */
      var frame = widgetFrameTemplate.replace("{widget-source}", widgetSource+urlOptions);
      var frameId = "frame-" + (totalLoaded);
      frame = frame.replace("{track-sc_id}", item.sc_id);
      frame = frame.replace("{frame-id}", frameId);
      
      /* Add widget to html */
      $('#tracks').append(frame);

      /* Set up autoplay when previous widget finishes (except for first) */
      if (totalLoaded > 0)
      {
        var prev_widget = SC.Widget('frame-'+(totalLoaded-1));
        var this_widget = SC.Widget('frame-'+(totalLoaded));
        prev_widget.bind(SC.Widget.Events.FINISH, function() {
          this_widget.play();
        });        
      }      
      
      totalLoaded += 1;
      
      /*tracks.push(track_row.replace('{track-sc_id}', item.sc_id).
                  replace('{track-target-permalink}', item.target_permalink).
                  replace('{track-target-permalink}', item.target_permalink).
                  replace('{image}', data.images[item.target_id])
                  );*/
    });
    if (typeof callback == "function"){
      callback();
    }
  });
}

/* Displays the button (hidden on page load) */
function displayButton() {
  $('#load-more').show();
}

function playFirst() {
  try {
    var widget = SC.Widget("frame-0");
    widget.bind(SC.Widget.Events.READY, function() {
      widget.play();
    });
  }
  finally {
    displayButton();
  } 
  
}

/* Runs when page is loaded */
$(function() {
  getMore(count, playFirst);
	$('#load-more').click( function() {
    getMore(count);
  });
});