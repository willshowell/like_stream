import soundcloud
from requests.exceptions import HTTPError
import config 

sc_client = soundcloud.Client(client_id=config.SOUNDCLOUD_CLIENT_ID)

def resolve_user_id(user_url):
    '''Converts a SoundCloud url to a user id'''
    # Convert to URL if not one already
    if 'soundcloud.com' not in user_url:
        user_url = "https://soundcloud.com/" + user_url
    try:
        user = sc_client.get('/resolve', url=user_url)
    except HTTPError:
        raise ValueError("SoundCloud user does not seem to exist")
    return user.id, user.permalink

def get_favorites(userid, limit):
    '''Gets most recent favorites from user with userid'''
    track_ids = []
    tracks = sc_client.get('/users/{}/favorites'.format(userid),
                               limit=limit, offset=0)
    for track in tracks:
        track_ids.append(track.id)
    return track_ids

def get_user_image(userid):
    '''Returns a string of the image url given a userid'''
    user = sc_client.get('/users/{}'.format(userid))
    if 'default' in user.avatar_url:
        return user.avatar_url
    else:
        return user.avatar_url.replace('large','t500x500')
