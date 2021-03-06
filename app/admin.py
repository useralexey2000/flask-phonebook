from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
from functools import wraps
from werkzeug.exceptions import abort
from app import db
from app.models import User, ACCESS
from app.forms import UserForm

bp = Blueprint('admin', __name__, url_prefix='/admin')

"""
    Decorators for accessing secure data
"""
def permission_required(permission):
    """Decorator for access based on permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator for admin access"""
    return permission_required(ACCESS['admin'])(f)

@bp.route('/users')
@bp.route('/users/<int:page>')
@login_required
@admin_required
def users(page=1):
    """Display all registered users"""
    users = User.query.order_by(User.id.desc()).paginate(page, per_page=30)
    return render_template('admin/users.html', users=users)

@bp.route('/users/create', methods=('GET', 'POST'))
@login_required
@admin_required
def user_create():
    """Create user"""
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(500)
        return redirect(url_for('admin.users'))
    return render_template('admin/user-create-edit.html', form=form, title='user-create')


@bp.route('/users/<id>/edit', methods=('GET', 'POST'))
@login_required
@admin_required
def user_edit(id):
    """Edit user"""
    user = User.query.get(id)
    if not user:
        abort(404, 'the page not found.')
    form = UserForm(request.form, obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.role = form.role.data
        if form.reset_password.data:
            user.password = form.password.data
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(500)
        return redirect(url_for('admin.users'))
    return render_template('admin/user-create-edit.html', form=form, title='user-edit')

    
@bp.route('/users/<id>/delete', methods=('POST',))
@login_required
@admin_required
def user_delete(id):
    """Delite user"""
    user = User.query.get(id)
    if not user:
        abort(404, 'the page not found.')
    db.session.delete(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(500)
    return redirect(url_for('admin.users'))