from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired



class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired()
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ])
    password2 = PasswordField(
        'Confirm Pasword',
        validators=[DataRequired()]
        )

class LoginForm(Form):
    email = StringField(
        'Email', 
        validators=[
            DataRequired()
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ])