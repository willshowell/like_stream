from flask import Flask, render_template


DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

app = Flask(__name__)


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
