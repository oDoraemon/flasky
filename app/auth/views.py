from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_required, login_user

from . import auth
from forms import LoginForm, RegisterForm
from .. import db
from ..models import User

@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    pass

@auth.route('/register')
def register():
    pass
