 
/*
<iframe class="grid-75" height="150" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{track-sc_id}&amp;auto_play=false&amp;hide_related=true&amp;show_comments=false&amp;show_user=true&amp;show_reposts=false&amp;visual=true">
<iframe id="sc-widget" src="https://w.soundcloud.com/player/?url=http://api.soundcloud.com/users/1539950/favorites" width="100%" height="465" scrolling="no" frameborder="no"></iframe>
*/


/* Keep track of how many tracks have been loaded */
var totalLoaded = 0;
var count = 5;

/* Load more tracks */
function getMore(loadCount, callback) {
  
  /* Send AJAX request */
  $.getJSON($SCRIPT_ROOT + '/_more', {
    start: totalLoaded,
    end: totalLoaded + loadCount
  }, function(data) {
    
    /* If no new tracks were loaded, display 'end' message */
    if (data.tracks.length == 0) {
      $('#end-stream').show();
    }
    
    console.log(data);
    
    /* Iterate through each track in the response */
    $.each( data.tracks, function( i, item ) {
      
      console.log(item);
      
      /* Generate a widget iframe */
      var frame = widgetFrameTemplate.replace("{widget-source}", widgetSource+urlOptions);
      var frameId = "frame-" + (totalLoaded);
      frame = frame.replace("{track-sc_id}", item.sc_id);
      frame = frame.replace("{frame-id}", frameId);
      
      /* Generate html row with user picture and iframe */
      var row = track_row.replace("{image}", data.images[item.target_id]);
      row = row.replace("{track-target-permalink}", item.target_permalink);
      row = row.replace("{track-target-permalink}", item.target_permalink);
      row = row.replace("{iframe}", frame)
      
      /* Add row to html */
      $('#tracks').append(row);

      /* Set up autoplay when previous widget finishes (except for first) */
      if (totalLoaded > 0)
      {
        var prev_widget = SC.Widget('frame-'+(totalLoaded-1));
        var this_widget = SC.Widget('frame-'+(totalLoaded));
        prev_widget.bind(SC.Widget.Events.FINISH, function() {
          this_widget.play();
        });        
      }      
      
      /* Increment counter */
      totalLoaded += 1;
    });
    
    /* Run callback if necessary */
    if (typeof callback == "function"){
      callback();
    }
    
  });
}

/* Displays the 'load more' button (hidden on page load) */
function displayButton() {
  $('#load-more').show();
}

/* Starts autoplay */
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

/* Run when page is loaded */
$(function() {
  
  /* Get initial tracks */
  getMore(count, displayButton);
  
  /* Get more tracks when button is pressed */
	$('#load-more').click(function() {
    getMore(count);
  });
  
});