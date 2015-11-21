from flask import Flask, g, render_template

import models, forms

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.database
    g.db.connect()
    g.user = current_user

@app.route('/')
def index():
    return 'Welcome to the Soundcloud likestream.'

@app.route('/login')
def login():
    return 'This is where a user will login.'

@app.route('/register')
def register():
    return 'This is where a new user will register.'

@app.route('/stream')
def stream():
    return 'This is where the stream of songs will be.'

@app.route('/user/<username>')
def user(username):
    return 'This is where the user profile for <em>{}</em> would be.'.format(username)

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
