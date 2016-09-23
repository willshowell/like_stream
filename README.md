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
