
/* Templates for generating each track iframe */
var widgetFrameTemplate = '<iframe class="grid-75 track" id="{frame-id}" \
                                   src="{widget-source}" frameborder="no" \
                                   scrolling="no" > \
                           </iframe>';
  
var widgetSource = "https://w.soundcloud.com/player/?" +
                   "url=https://api.soundcloud.com/tracks/{track-sc_id}";
                    
var urlOptions = "&amp;auto_play=false&amp;hide_related=true&amp;" +
                 "show_comments=false&amp;show_user=true&amp;" +
                 "show_reposts=false&amp;visual=true";
                  
                  
/* Template for each track row */
var track_row = ' <div class="row"> \
                    <div class="grid-25 track" style="margin-right: 5px; height: 150px; width: 150px; background-size: 100%;background-image: url({image});"> \
                      <a href="http://soundcloud.com/{track-target-permalink}"><span class="sc-style">{track-target-permalink}\'s like</span></a> \
                    </div> \
                    {iframe} \
                  </div> \
                  <br> \
                ';