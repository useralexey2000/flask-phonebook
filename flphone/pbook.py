from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .forms import PhoneForm, ContactForm
from .db import mongo
from bson.objectid import ObjectId

bp = Blueprint('pbook', __name__)


@bp.route('/')
def index():
    col = mongo.db.fphone
    res = list(col.find())
    return render_template('pbook/index.html', pbook_list=res)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form  = ContactForm(request.form)   
    if request.method == 'POST':
        if form.validate_on_submit():
            col = mongo.db.fphone
            entry = {}
            entry['uname'] = form.uname.data
            entry['fname'] = form.fname.data
            entry['lname'] = form.lname.data
            entry['dep'] = form.dep.data
            entry['pos'] = form.pos.data
            entry['phones'] = form.phones.data
            col.save(entry)
            return redirect('/')
    return render_template('pbook/create-edit.html', form=form, title='phone-create')


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    col = mongo.db.fphone
    res = col.find_one({'_id': ObjectId(id)})
    if not res:
        abort(404, 'the page not found.')
    if request.method == 'POST':
        form = ContactForm(request.form)
        if form.validate_on_submit():
            entry = {}
            entry['uname'] = form.uname.data
            entry['fname'] = form.fname.data
            entry['lname'] = form.lname.data
            entry['dep'] = form.dep.data
            entry['pos'] = form.pos.data
            entry['phones'] = form.phones.data
            col.update_one({'_id': ObjectId(id)}, {'$set': entry })
            return redirect('/')
    form = ContactForm(data=res)
    return render_template('pbook/create-edit.html', form=form, title='phone-edit')


@bp.route('/<id>/delete', methods=('POST',))
def delete(id):
    col = mongo.db.fphone
    res = col.find_one({'_id': ObjectId(id)})
    if not res:
        abort(404, 'the page not found.')
    col.delete_one({'_id': ObjectId(id)})
    return redirect('/')
    



