import datetime, os

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *
from random import shuffle


'''DATABASE = 'like_stream.db'

# generate a peewee database instance
database = SqliteDatabase(DATABASE) '''

database = Proxy()

# base model class that all others will extend
class BaseModel(Model):
    class Meta:
        database = database


# each user of this app
# users are many-to-many with targets
class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    def targets(self):
        return (Target
                .select()
                .join(UserTarget)
                .where(UserTarget.user == self)
                .order_by(UserTarget.added_at.desc()))

    def stream(self, begin, end):
        tracks =[]
        targets = self.targets()
        for target in targets:
            tracks.extend(target.get_tracks())
        tracks.sort(key= lambda track: track.liked_at, reverse=True)
        return tracks[begin:end]

    @classmethod
    def create_user(cls, username, password, admin=False):
        try:
            with database.transaction():
                return cls.create(
                    username=username,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


# each unique soundcloud user
# targets are many-to-many with users
# 
class Target(BaseModel):
    sc_id = BigIntegerField(unique=True)
    permalink = CharField()
    added_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def get_tracks(self):
        return Track.select().where(Track.target == self).order_by(-Track.liked_at)

    def update_time(self):
        self.updated_at = datetime.datetime.now()

    @classmethod
    def create_target(cls, sc_id, permalink):
        try:
            with database.transaction():
                return cls.create(sc_id=sc_id, permalink=permalink)
        except IntegrityError:
            raise ValueError("Target already exists")


# models a many-to-many between targets and users
# creating a new relationship checks to make sure
# one didn't already exist
class UserTarget(BaseModel):
    user = ForeignKeyField(User)
    target = ForeignKeyField(Target)
    added_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def create_usertarget(cls, user, target):
        try:
            UserTarget.get( UserTarget.user == user, UserTarget.target == target)
            raise ValueError("Relationship already exists")
        except DoesNotExist:
            with database.transaction():
                cls.create(user=user, target=target)

    @classmethod
    def delete_usertarget(cls, user, target):
        try:
            desired_ut = UserTarget.get( UserTarget.user == user, UserTarget.target == target)
            desired_ut.delete_instance()
        except DoesNotExist:
            raise ValueError("Relationship did not exist")

# a track liked by one of the targets
# tracks are many-to-one with target
# they are not unique, because multiple targets could
# like the same song, but add them at different times
# [todo] maybe they should be unique at some point
class Track(BaseModel):
    sc_id = BigIntegerField(unique=False)
    liked_at = DateTimeField(default=datetime.datetime.now)
    target = ForeignKeyField(
        rel_model=Target,
        related_name='tracks'
    )


# set up the database proxy based on the environment
# if running locally, use sqlite
# if running on heroku, use postgesql
if 'HEROKU' in os.environ:
    import urllib.parse, psycopg2
    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    db = PostgresqlDatabase(database=url.path[1:], user=url.username, 
        password=url.password, host=url.hostname, port=url.port)
    database.initialize(db)
else:
    db = SqliteDatabase('like_stream.db')
    database.initialize(db)

def initialize():
    database.connect()
    database.create_tables([User, Target, UserTarget, Track], safe=True)
    database.close()