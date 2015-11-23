import soundcloud

from secrets import SOUNDCLOUD_CLIENT_ID

scid = SOUNDCLOUD_CLIENT_ID

client = soundcloud.Client(
	client_id=scid)


username='will-howell-1'

user = client.get('/resolve', url='http://soundcloud.com/{}'.format(username))


print("User {} has {} likes!".format(user.id, user.public_favorites_count) )


favorites_left = user.public_favorites_count
favorites = []
while (favorites_left):
	offset = user.public_favorites_count - favorites_left
	print("Trying to get from offset {}".format(offset))
	returned_favorites = client.get('/users/{}/favorites'.format(user.id), offset=offset)
	print("Received {} faves".format(len(returned_favorites)))
	favorites.extend(returned_favorites)
	favorites_left -= len(returned_favorites)
	if favorites_left < 1:
		break

for favorite in favorites:
	print("{} - {}".format(favorite.id, favorite.title))