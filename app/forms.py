from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList, FormField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField
from app.models import User, ACCESS


class PhoneForm(FlaskForm):
    num = IntegerField('phone:', [DataRequired()])
    class Meta:
        csrf = False

class ContactForm(FlaskForm):
    uname = StringField('first name:', [DataRequired(), Length(min=4, max=30)])
    fname = StringField('father\'s name:', [DataRequired(), Length(min=4, max=30)])
    lname = StringField('last name:', [DataRequired(), Length(min=4, max=30)])
    dep = StringField('department:', [DataRequired(), Length(min=4, max=30)])
    pos = StringField('position:', [DataRequired(), Length(min=4, max=30)])
    phones = FieldList(FormField(PhoneForm), min_entries=1, max_entries=5)
    submit = SubmitField('save')

class LoginForm(FlaskForm):
    email = EmailField('email:', [DataRequired(), Email()])
    password = PasswordField('password:', [DataRequired(), Length(max=20)])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('login')


class RegisterForm(FlaskForm):
    email = EmailField('email:', [DataRequired(), Email(), Length(max=100)])
    password = PasswordField('password:', [DataRequired(), EqualTo('password2') , Length(max=20)])
    password2 = PasswordField('confirm password:', [DataRequired(), Length(max=20)])
    submit = SubmitField('register')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('email already registered')


