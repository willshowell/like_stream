from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Length, EqualTo, 
                                Email, Regexp)


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            )
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
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
    email = StringField(
        'Email', 
        validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ])