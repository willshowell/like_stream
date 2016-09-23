import time, datetime
import soundcloud_helper as sch 
from app import models
from config import DEBUG

def update_target_in_db(target, amount=5):
    """Update Target

    Uses SoundCloud API to get a list of the most 
    recent `amount` of likes for the `target`. That
    list is compared to the existing list of tracks
    the target has liked, and  the difference is
    added to the list of likes for the target.
    """
    if DEBUG:
        print("Updating: {}, id={}".format(target.permalink, target.sc_id))
        print("Last updated at: {}".format(target.updated_at))

    # Figure out how many new likes have
    # occurred since the last check
    prev_faves = []
    for track in target.get_tracks():
        prev_faves.append(track.sc_id)
    new_faves = sch.get_favorites(target.sc_id, amount)

    # If new songs liked:
    #   prev = [6, 5, 4, 3, 2, 1, 0]
    #   new  = [8, 7, 6, 4, 3]
    # Then:
    #   diff = [8, 7]
    diff = [item for item in new_faves if item not in prev_faves]
    diff.reverse()
    if DEBUG:
        print("Need to add {}.".format(diff))

    # Track `liked_at` times are distributed evenly
    # since the last time the target was updated.
    for index, track in enumerate(diff):
        
        old_time = target.updated_at
        new_time = datetime.datetime.now()
        
        split = (index+1)/len(diff)
        split_time = old_time + split * (new_time - old_time)
        
        if DEBUG:
            print("Adding {} at {}".format(track, split_time))
        
        models.Track.create(
            sc_id = track,
            target = target,
            liked_at = split_time)


#
# Worker process
# 
# Iterates through every target stored in the
# database and updates it.
if __name__ == '__main__':
    models.database.connect()
    targets = models.Target.select()
    for target in targets:
        update_target_in_db(target)
        target.update_time()
        target.save()

    models.database.close()
