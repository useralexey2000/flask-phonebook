from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange, Length
import uuid


bp = Blueprint('pbook', __name__)

pbook_list = [
    {   
        "id": "03363e5a9d9c4f1ca7a8dc465116c370",
        "uname": "user1",
        "fname": "fuser1",
        "lname": "luser1",
        "dep": "dep1",
        "pos": "pos1",
        "phones": [
            {"phone": 1111},
            {"phone": 2222},
            {"phone": 3333},
        ],
    },
    {
        "id": "37ab474c0d3c4ed0ba2b08ac99a738b5",
        "uname": "user2",
        "fname": "fuser2",
        "lname": "luser2",
        "dep": "dep1",
        "pos": "pos2",
        "phones": [
            {"phone": 4444},
        ]
    },
    # {
    #     "id": "92c962e9587e45218707c38f1cc143e3",
    #     "uname": "user3",
    #     "fname": "fuser3",
    #     "lname": "luser3",
    #     "dep": "dep1",
    #     "pos": "pos3",
    #     "phones": [555, 666]
    # },
    # {
    #     "id": "f34ebced615e41e9bca5ca09039f5254",
    #     "uname": "user4",
    #     "fname": "fuser4",
    #     "lname": "luser4",
    #     "dep": "dep1",
    #     "pos": "pos4",
    #     "phones": [777]
    # },
]

class PhoneForm(FlaskForm):
    phone = IntegerField('phone:', [DataRequired()])
    class Meta:
        csrf = False

class ContactForm(FlaskForm):
    uname = StringField('first name:', [DataRequired(), Length(min=4, max=10)])
    fname = StringField('father\'s name:', [DataRequired(), Length(min=4, max=10)])
    lname = StringField('last name:', [DataRequired(), Length(min=4, max=20)])
    dep = StringField('department:', [DataRequired(), Length(min=4, max=20)])
    pos = StringField('position:', [DataRequired(), Length(min=4, max=30)])
    phones = FieldList(FormField(PhoneForm), min_entries=1, max_entries=5)
    removep = SubmitField('remove')
    addp = SubmitField('add')
    submit = SubmitField('save')


@bp.route('/')
def index():
    return render_template('pbook/index.html', pbook_list=pbook_list)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form  = ContactForm(request.form)

    if request.method == 'POST':
        
        # if form.addp.data:
        #     form.phones.append_entry()
        #     form.addp.data = False
        #     return render_template('pbook/create-edit.html', form=form)
        # if form.removep.data:
        #     form.phones.pop_entry()
        #     form.removep.data = False
        #     return render_template('pbook/create-edit.html', form=form)
        if form.validate_on_submit():
            entry = {}
            entry['id'] = uuid.uuid4().hex
            entry['uname'] = form.uname.data
            entry['fname'] = form.fname.data
            entry['lname'] = form.lname.data
            entry['dep'] = form.dep.data
            entry['pos'] = form.pos.data
            entry['phones'] = [form.phones.data]
            pbook_list.append(entry)
            return redirect('/')
    return render_template('pbook/create-edit.html', form=form, title='phone-create')


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    res = [i for i in pbook_list if i['id'] == id]
    if res:
        if request.method == 'POST':
            pass
            # form = ContactForm(request.form)
            # if form.addp.data:
            #     form.phones.append_entry()
            #     return render_template('pbook/edit.html', form=form)
            # if form.removep.data:
            #     form.phones.pop_entry()
            #     return render_template('pbook/edit.html', form=form)
            # if form.validate_on_submit():
            #     return redirect('/')
        form = ContactForm(data=res[0])
        return render_template('pbook/create-edit.html', form=form, title='phone-edit')


@bp.route('/<id>/delete', methods=('POST',))
def delete(id):
    res = [i for i in pbook_list if i['id'] == id]
    if res:
        pbook_list.remove(res[0])
    return redirect('/')

    


