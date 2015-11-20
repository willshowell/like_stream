
from peewee import *


DATABASE = SqliteDatabase('like_stream.db')

class User(Model):
    username = CharField(unique=True)