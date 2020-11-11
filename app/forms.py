from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList, FormField, PasswordField, BooleanField, ValidationError, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField
from app.models import User, ACCESS


class PhoneForm(FlaskForm):
    """Phone form"""
    num = IntegerField('phone:', [DataRequired(message='Field cant be blank')])
    class Meta:
        csrf = False

class ContactForm(FlaskForm):
    """Contact form"""
    uname = StringField('first name:', [DataRequired(message='Field cant be blank'), Length(min=4, max=30, message='Field lenght: min=4, max=30'),])
    fname = StringField('father\'s name:', [DataRequired(message='Field cant be blank'), Length(min=4, max=30, message='Field lenght: min=4, max=30')])
    lname = StringField('last name:', [DataRequired(message='Field cant be blank'), Length(min=4, max=30, message='Field lenght: min=4, max=30')])
    dep = StringField('department:', [DataRequired(message='Field cant be blank'), Length(min=4, max=30, message='Field lenght: min=4, max=30')])
    pos = StringField('position:', [DataRequired(message='Field cant be blank'), Length(min=4, max=30, message='Field lenght: min=4, max=30')])
    phones = FieldList(FormField(PhoneForm), min_entries=1, max_entries=5)
    submit = SubmitField('save')

class LoginForm(FlaskForm):
    """Login form"""
    email = EmailField('email:', [DataRequired(message='Field cant be blank'), Email(message='Not correct email'), Length(max=100, message='Field lenght: max=100')])
    password = PasswordField('password:', [DataRequired(message='Field cant be blank'), Length(max=20, message='Field lenght: max=20')])
    remember_me = BooleanField('keep me logged in:')
    submit = SubmitField('login')


class RegisterForm(FlaskForm):
    """Register form"""
    email = EmailField('email:', [DataRequired(message='Field cant be blank'), Email(message='Not correct email'), Length(max=100, message='Field lenght: max=100')])
    password = PasswordField('password:', [DataRequired(message='Field cant be blank'), EqualTo('password2', message='Passwords don\'t match') , Length(max=20, message='Field lenght: max=20')])
    password2 = PasswordField('confirm password:', [DataRequired(message='Field cant be blank'), Length(max=20, message='Field lenght: max=20')])
    submit = SubmitField('register')

    def validate_email(self, field):
        """Check if email already exists in databese"""
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('email already registered')


class UserForm(FlaskForm):
    """User form"""
    email = EmailField('email:', [DataRequired(message='Field cant be blank'), Email(message='Not correct email'), Length(max=100, message='Field lenght: max=100')])
    reset_password = BooleanField('change password:')
    password = PasswordField('password:', [Length(max=20, message='Field lenght: max=20')])
    role = SelectField('role:', choices=[i for i in ACCESS.keys()])
    submit = SubmitField('save')