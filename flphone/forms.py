from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList, FormField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length, Email
from wtforms.fields.html5 import EmailField


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
    submit = SubmitField('save')

class LoginForm(FlaskForm):
    email = EmailField('email', [DataRequired(), Email()])
    password = PasswordField('password:', [DataRequired(), Length(max=20)])
    submit = SubmitField('login')