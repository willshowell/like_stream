from flask import Flask, g, render_template, redirect, url_for, flash, request
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, current_user,
                             login_required, logout_user)
from secrets import APP_SECRET_KEY

import soundcloud_helper as sch

import models, forms

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

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
    if current_user.is_authenticated:
        flash("You've been logged out.", "success")
        logout_user()
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
                flash("Your email and password do not match.", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    flash("You've been logged out.", "success")
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        flash("You've been logged out.", "success")
        logout_user()
    form = forms.RegisterForm()
    if form.validate_on_submit():
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        return redirect(url_for('stream'))
    return render_template('register.html', form=form)

@app.route('/stream')
@login_required
def stream():
    stream = current_user.stream()

    target_image_dict = {}
    for target in current_user.targets():
        image_url = sch.get_user_image(target.sc_id)
        target_image_dict[target.sc_id] = image_url

    return render_template('stream.html', stream=stream, images=target_image_dict)

@app.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    targets = current_user.targets()
    new_target_form = forms.TargetForm()
    if new_target_form.validate_on_submit():
        # Try to resolve the username
        try:
            user_id, permalink=sch.resolve_user_id(new_target_form.sc_user_profile.data)
        except ValueError:
            flash("This user doesn't seem to exist. Try a different name.", "error")
            return render_template('profile.html',
                                   form=new_target_form,
                                   targets=targets)

        # Create a target from that id if it doesn't already exist
        try:
            models.Target.create_target(
                sc_id=user_id,
                permalink=permalink
            )
            #TODO get, store, and datetime this target's favorites
            flash("This user is now being tracked.", "success")
        except ValueError:
            flash("This user is already being tracked.", "message")
            pass

        # Map the current user to that target
        try:
            models.UserTarget.create_usertarget(
                user=g.user._get_current_object(),
                target=models.Target.get(
                    models.Target.sc_id == user_id
                )
            )
            flash("You are now following them.", "success")
        except ValueError:
            flash("You are already following this user.", "error")

    return render_template('profile.html', 
                           new_target_form=new_target_form, 
                           targets=targets)

@app.route('/delete_target', methods=['GET','POST'])
@login_required
def delete_target():
    if request.method != 'POST':
        return redirect(url_for('profile'))

    # Remove usertarget link
    try:
        models.UserTarget.delete_usertarget(
            user=g.user._get_current_object(),
            target=models.Target.get(
                models.Target.sc_id == request.form['target']
            )
        )
        flash("You are no longer following this user.", "success")
    except ValueError:
        flash("Error removing this user.", "error")
    return redirect(url_for('profile'))

@app.route('/about')
def help():
    return render_template('help.html')


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
