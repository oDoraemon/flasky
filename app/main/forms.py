from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Required, Email
from .. import db

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[Required()])
    submit = SubmitField("Submit")
