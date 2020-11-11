from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import abort
from app.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Login user"""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect('/')
        flash('invalid username or password.')
    return render_template('auth/login.html', form=form, title='login')


@bp.route('/logout', methods=('GET', 'POST'))
@login_required
def logout():
    """Logout logged in user"""
    logout_user()
    flash('you have been logged out.')
    return redirect('/')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register user"""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(500)
        flash('you successfuly registered account.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title='register')

