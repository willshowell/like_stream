import soundcloud

from secrets import SOUNDCLOUD_CLIENT_ID

scid = SOUNDCLOUD_CLIENT_ID

client = soundcloud.Client(
	client_id=scid)

def resolve_user_id(username):
	user = client.get('/resolve', url='http://soundcloud.com/{}'.format(username))
	return user.id

def get_track_name(track_id):
	track = client.get('/tracks/{}'.format(track_id))
	return track.title

def get_favorites_count(user_id):
	user = client.get('/users/{}'.format(user_id))
	return user.public_favorites_count

def get_favorites_list(user_id):
	count = get_favorites_count(user_id)
	favorites_left = count
	favorites = []
	while favorites_left > 0:
		offset = count - favorites_left
		returned_favorites = client.get('/users/{}/favorites'.format(user_id), 
		                                offset=offset,
		                                limit=20)
		for favorite in returned_favorites:
			favorites.append(favorite.id)
		favorites_left -= len(returned_favorites)
	return favorites

name='will-howell-1'
userid = resolve_user_id(name)
print(userid)

user = client.get('/users/{}'.format(userid))
print(user.avatar_url)

'''
ids = get_favorites_list(userid)
print(ids)
print(len(ids))
for track in ids:
	print(get_track_name(track))
'''

'''
favorites_left = count
favorites = []
while (favorites_left):
	offset = count - favorites_left
	returned_favorites = client.get('/users/{}/favorites'.format(userid), offset=offset)
	favorites.extend(returned_favorites)
	favorites_left -= len(returned_favorites)
	if favorites_left < 1:
		break

ct = 0
for favorite in favorites:
	ct+=1
	print("{} - {}".format(ct, favorite.title))'''