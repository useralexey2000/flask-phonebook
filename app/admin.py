from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import current_user, login_required
from functools import wraps
from werkzeug.exceptions import abort
from app import db
from app.models import User, ACCESS
from app.forms import UserForm

bp = Blueprint('admin', __name__, url_prefix='/admin')

"""Decorators for accessing secure data"""
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(ACCESS['admin'])(f)

@bp.route('/users')
@bp.route('/users/<int:page>')
@login_required
@admin_required
def users(page=1):
    # users = User.query.all()
    users = User.query.order_by(User.id.desc()).paginate(page, per_page=30)
    return render_template('admin/users.html', users=users)

@bp.route('/users/create', methods=('GET', 'POST'))
@login_required
@admin_required
def user_create():
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.users'))
    return render_template('admin/user-create-edit.html', form=form, title='user-create')


@bp.route('/users/<id>/edit', methods=('GET', 'POST'))
@login_required
@admin_required
def user_edit(id):
    user = User.query.get(id)
    if not user:
        abort(404, 'the page not found.')
    form = UserForm(request.form, obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.role = form.role.data
        if form.reset_password.data:
            user.password = form.password.data
        db.session.commit()
        return redirect(url_for('admin.users'))
    return render_template('admin/user-create-edit.html', form=form, title='user-edit')

    
@bp.route('/users/<id>/delete', methods=('POST',))
@login_required
@admin_required
def user_delete(id):
    user = User.query.get(id)
    if not user:
        abort(404, 'the page not found.')
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.users'))