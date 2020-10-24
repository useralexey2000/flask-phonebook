from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .forms import PhoneForm, ContactForm
from app import db
from app.models import Contact, Phone, User

bp = Blueprint('pbook', __name__)

@bp.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('pbook/index.html', contacts=contacts)


@bp.route('/create', methods=('GET', 'POST'))
def create():
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
        db.session.commit()
        return redirect('/')

    return render_template('pbook/create-edit.html', form=form, title='phone-create')


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    contact = Contact.query.get(id)
    if not contact:
        abort(404, 'the page not found.')
    form = ContactForm(request.form)
    if form.validate_on_submit():
        phones = [Phone(num = i.num.data, contact_id = id) for i in form.phones]

        phones_to_del = [ i for i in contact.phones if i not in phones]
        for i in phones_to_del: db.session.delete(i)
        phones_to_add = [i for i in phones if i not in contact.phones]
        for i in phones_to_add: db.session.add(i)

        contact.uname = form.uname.data
        contact.fname = form.fname.data
        contact.lname = form.lname.data
        contact.dep = form.dep.data
        contact.pos = form.pos.data
        db.session.commit()
        return redirect('/')

    form = ContactForm(obj=contact)
    return render_template('pbook/create-edit.html', form=form, title='phone-edit')


@bp.route('/<id>/delete', methods=('POST',))
def delete(id):
    contact = Contact.query.get(id)
    if not contact:
        abort(404, 'the page not found.')
    db.session.delete(contact)
    db.session.commit()
    return redirect('/')