import datetime, os
from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *
from random import shuffle
import json

from config import DATABASE


# Initialize the database based on credentials from config file
database = PostgresqlDatabase(DATABASE['NAME'], 
                             user = DATABASE['USER'], 
                             password = DATABASE['PASSWORD'],
                             host = DATABASE['HOST'],
                             port = DATABASE['PORT'])


class BaseModel(Model):
    """A base model that will user the Postgresql database"""
    class Meta:
        database = database


class User(UserMixin, BaseModel):
    """User model
    
    Each user has login credentials, admin status, and 
    join time. Users have a many-to-many relationship
    with targets.
    """
    username = CharField(unique = True)
    password = CharField(max_length = 100)
    joined_at = DateTimeField(default = datetime.datetime.now)
    is_admin = BooleanField(default = False)

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


class Target(BaseModel):
    """Target model

    A target is a representation of a SoundCloud user.
    The target's SoundCloud UID and SoundCloud permalink
    are stored in the model, as well as date added and 
    date updated. Targets have a many-to-many relationship
    with users.
    """
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


class UserTarget(BaseModel):
    """UserTarget relationship model

    Users and targets have a many-to-many relationship
    with eachother. The UserTarget model tracks those
    relationships.
    """
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


class Track(BaseModel):
    """Track model

    A track is a representation of a SoundCloud track.
    In addition to storing the SoundCloud UID of the 
    track, it contains the time it was "liked" and the 
    target, or SoundCloud user, who "liked" it. It is
    not unique because multiple targets could like the
    same track.
    """
    sc_id = BigIntegerField(unique=False)
    liked_at = DateTimeField(default=datetime.datetime.now)
    target = ForeignKeyField(
        rel_model=Target,
        related_name='tracks'
    )

    def serialize(self):
        return {
            'sc_id': self.sc_id,
            'target_id': self.target.sc_id,
            'target_permalink': self.target.permalink,
        }


def create_tables():
    """Helper function to be run one time from the shell"""
    database.connect()
    database.create_tables([User, Target, UserTarget, Track], safe=True)
    database.close()
