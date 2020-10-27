from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from .forms import LoginForm
from .db import db


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
        pass

    return render_template('auth/login.html', form=form, title='login')


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    pass

@bp.route('/register', methods=('GET', 'POST'))
def register():
    pass
