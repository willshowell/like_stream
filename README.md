# SoundCloud Like Stream

Check it out [live](http://soundcloudlikes.herokuapp.com)!

This site was built as an experiment in using the SoundCloud public API along 
with Flask.

### TODO
- Add tests
- Reformat profile page
- Make stream CSS prettier
- Make worker process more robust for unlikes
- Implement search
- Add 404 page


## Running
```
gunicorn -b 127.0.0.1:8000 app:app
```

Also set up a cron job to run the background worker process. In order to have it check for
new updates every 15 minutes, add the following to your crontab:

```
*/15 * * * * /full/path/to/env/bin/python /full/path/to/project/worker.py
```
