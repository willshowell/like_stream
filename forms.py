from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Length, EqualTo, 
                                Email, Regexp, ValidationError)

from models import User

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            name_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('confirm', message='Passwords must match.')
        ])
    confirm = PasswordField(
        'Confirm Pasword',
        validators=[DataRequired()]
        )

class LoginForm(Form):
    username = StringField(
        'Username', 
        validators=[
            DataRequired(),
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ])

class TargetForm(Form):
    sc_user_profile = StringField(
        'SoundCloud Profile Permalink',
        validators=[
            DataRequired()
        ])