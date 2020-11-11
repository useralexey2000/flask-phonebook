from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import abort
from .forms import PhoneForm, ContactForm
from app import db
from app.models import Contact, Phone, User
from flask_login import login_required

bp = Blueprint('pbook', __name__)

@bp.route('/')
@bp.route('/<int:page>')
def index(page=1):
    """Display all contacts"""
    contacts = Contact.query.order_by(Contact.lname.asc()).paginate(page, per_page=30)
    return render_template('pbook/index.html', contacts=contacts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create contact"""
    form  = ContactForm(request.form)
    if form.validate_on_submit():
        print('validate on sub')
        phones = [Phone(num = i.num.data) for i in form.phones]
        contact = Contact(uname = form.uname.data,
                          fname = form.fname.data,
                          lname = form.lname.data,
                          dep = form.dep.data,
                          pos = form.pos.data,
                          phones = phones)
        db.session.add(contact)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(500)
        return redirect('/')

    return render_template('pbook/create-edit.html', form=form, title='phone-create')


@bp.route('/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    """Edit contact"""
    contact = Contact.query.get(id)
    if not contact:
        abort(404, 'the page not found.')
    form = ContactForm(request.form, obj=contact)
    if form.validate_on_submit():
        # Current phones
        phones = [Phone(num = i.num.data, contact_id = id) for i in form.phones]

        # Phones to delete
        phones_to_del = [ i for i in contact.phones if i not in phones]
        for i in phones_to_del: db.session.delete(i)
        # Add new phones
        phones_to_add = [i for i in phones if i not in contact.phones]
        for i in phones_to_add: db.session.add(i)

        contact.uname = form.uname.data
        contact.fname = form.fname.data
        contact.lname = form.lname.data
        contact.dep = form.dep.data
        contact.pos = form.pos.data
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(500)
        return redirect('/')

    return render_template('pbook/create-edit.html', form=form, title='phone-edit')


@bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete contact"""
    contact = Contact.query.get(id)
    if not contact:
        abort(404, 'the page not found.')
    db.session.delete(contact)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(500)
        return redirect('/')
    return redirect('/')