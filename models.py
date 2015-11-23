import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = 'like_stream.db'

# generate a peewee database instance
database = SqliteDatabase(DATABASE)

# base model class that all others will extend
class BaseModel(Model):
    class Meta:
        database = database


# each user of this app
# users are many-to-many with targets
class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    def get_targets(self):
        pass

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with database.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


# each unique soundcloud user
# targets are many-to-many with users
class Target(BaseModel):
    sc_id = BigIntegerField(unique=True)
    added_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def create_target(cls, id):
        try:
            with database.transaction():
                cls.create(sc_id=id)
        except IntegrityError:
            raise ValueError("Target already exists")


# models a many-to-many between targets and users
class UserTarget(BaseModel):
    user = ForeignKeyField(User)
    target = ForeignKeyField(Target)


# a track liked by one of the targets
# tracks are many-to-one with target
class Track(BaseModel):
    sc_id = BigIntegerField(unique=False)
    liked_at = DateTimeField(default=datetime.datetime.now)
    target = ForeignKeyField(
        rel_model=Target,
        related_name='tracks'
    )


def initialize():
    database.connect()
    database.create_tables([User, Target, UserTarget, Track], safe=True)
    database.close()