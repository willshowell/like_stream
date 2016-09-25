# SoundCloud Like Stream

Check it out [live](http://soundcloud-likes.willshowell.com)!

This site was built as an experiment in using the SoundCloud public API along 
with Flask.


## Installation

Create a virtual environment:

```
$ mkvirtualenv like-stream --python=python3
```

Install dependencies:

```
$ pip install -r requirements.txt
```

Create a local PostgreSQL databse:

```
$ psql
-> CREATE DATABASE dbname;
-> CREATE USER username WITH PASSWORD password;
-> GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
-> \q
```

Create a `config.py` file in the root directory:

```python
DEBUG = True

DATABASE = {
  'NAME': 'dbname',
  'USER': 'username',
  'PASSWORD': 'password',
  'HOST': 'localhost',
  'PORT': ''
}

SECRET_KEY = '<some secret key>'

SOUNDCLOUD_CLIENT_ID = '<your api key>'
```





## Running

### Development
To run the devlopment server:

```
$ python run.py
```

To run the background update process:

```
$ python worker.py
```

### Production
To run the production server:

```
$ gunicorn -b 127.0.0.1:8000 app:app
```

To run the background process every 15 minutes, add
the following to your crontab (`$ crontab -e`):

```
*/15 * * * * /full/path/to/env/bin/python /full/path/to/project/worker.py
```



