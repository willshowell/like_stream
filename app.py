from flask import Flask, g, render_template, redirect, url_for, flash
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, current_user,
                             login_required, logout_user)

import models, forms

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

app = Flask(__name__)
app.secret_key = 'temp_secret_key'

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

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('stream'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email and password do not match.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match.", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('stream'))
    return render_template('register.html', form=form)

@app.route('/stream')
@login_required
def stream():
    return render_template('stream.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='will',
            email='will.s.howell@gmail.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
