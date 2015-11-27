import soundcloud_helper as sch, models
import time, datetime

if __name__ == '__main__':
	while True:

		#collect some stuff
		print("\nCollecting new data...\n")
		
		models.database.connect()
		targets=models.Target.select()
		for target in targets:
			print(target.permalink)

			#Get a list of the previous favorites (from database)
			prev_favorites = target.get_tracks()

			print("There are {} previous favorites".format(prev_favorites.count()))

			#Get a list of the current favorites (from Soundcloud)
			favorites = sch.get_favorites(target.sc_id, 5)
			
			# If there are no previous, save the current ones!
			if prev_favorites.count() == 0:
				for track in favorites:
					print("Adding {} to db".format(track))
					models.Track.create(
						sc_id = track,
						target = target
					)

			for track in favorites:
				print('  '+str(track))

		models.database.close()


		#wait some time
		time.sleep(10)