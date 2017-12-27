from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager, Shell
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Required, Email
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_mail import Mail
from datetime import datetime
from threading import Thread
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://cc_user:AmzRedGsvcAdminAcc@127.0.0.1:3306/gsvcdatabase"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['FLAKSY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Amdin <flask@example.com>'

bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data, id_role=2)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template("index.html", current_time=datetime.utcnow(),
                            form = form, name = session.get('name'),
                            known = session.get('known', False))

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    username = None
    email = None
    password = None
    form = UserForm()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email is None:
            user = User(username = form.username.data,
                        email = form.email.data,
                        password_hash = generate_password_hash(form.password_hash.data),
                        id_role = form.id_role.data,
                        confirmed = 1,
                        name = form.name.data,
                        location = 'China',
                        about_me = "user"
                        )
            db.session.add(user)
        else:
            flash("Email occupied!")

        return redirect(url_for('add_user'))
    all_user = User.query.all()
    return render_template("add_user.html", all_user = all_user, form = form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

class UserForm(FlaskForm):
    username = StringField("username", validators=[Required()])
    email = StringField("Email", validators=[Required(), Email()])
    password_hash = PasswordField("Password", validators=[Required()])
    id_role = IntegerField("Role", validators=[Required()])
    name = StringField("Name")
    submit = SubmitField("Create")


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[Required()])
    submit = SubmitField("Submit")

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    id_role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    confirmed = db.Column(db.Integer)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == '__main__':
    manager.run()
