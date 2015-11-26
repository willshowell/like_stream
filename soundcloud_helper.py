import soundcloud
from requests.exceptions import HTTPError
from secrets import SOUNDCLOUD_CLIENT_ID

sc_client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)

def resolve_user_id(username):
    '''Converts a SoundCloud username to a user id'''
    user_url = "http://soundcloud.com/{}".format(username)
    try:
        user = sc_client.get('/resolve', url=user_url)
    except HTTPError:
        raise ValueError("SoundCloud user does not seem to exist")
    return user.id, user.permalink

