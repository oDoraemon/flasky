from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringFi eld('Email', validators=[Required(), Length(1,64),
                        Email()])
    password = PasswordField('Password', validators=[Required()])
    remeber_me = BooleanField('Keep me logged in') 
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    msg = 'Usernames must have only letters, numbers, dots or underscores'
    email = StringField('Email', validators=[Required(), Length(1,64),
                        Email()])
    username = StringField('Username', validators=[
        Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0*9_.]*$', 0, msg)
    ])
    password = PasswordField('Password')