from wtforms import StringField, SubmitField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import Required, Email, Length
from .. import db

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Required(), Email(), Length(1, 64)])
    password = PasswordField("Password", validators=[Required()])
    remeber_me = BooleanField("Remeber Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    pass