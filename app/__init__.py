from flask import Flask
from config import SECRET_KEY

# Define the WSGI application object
app = Flask(__name__)
app.secret_key = SECRET_KEY

from app import controller
