from app import db, bcrypt, login_manager
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app


ACCESS = {
    # 'guest': 0,
    'user': 0,
    'admin': 1
}


class Contact(db.Model):
    """Contact model"""
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    dep = db.Column(db.String(150), nullable=False)
    pos = db.Column(db.String(150), nullable=False)
    phones = db.relationship('Phone', backref='phones', lazy=True, cascade="all, delete")
    def __repr__(self):
        return f'<Contact {self.id}>'


class Phone(db.Model):
    """Phone model"""
    __tablename__ = 'phones'
    num = db.Column(db.Integer(), primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    def __repr__(self):
        return f'<Phone {self.num}>'
    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.num == other.num


class User(db.Model, UserMixin):
    """User model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    access = db.Column(db.Integer)
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == current_app.config['SITE_ADMIN']:
            self.access = ACCESS['admin']
        else:
            self.access = ACCESS['user']
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    @property
    def role(self):
        return list(ACCESS.keys())[list(ACCESS.values())[self.access]]
    @role.setter
    def role(self, role):
        self.access = ACCESS[role]
    def can(self, permission):
        return self.access >= permission
    def __repr__(self):
        return f'<User {self.id}>'

class AnonymousUser(AnonymousUserMixin):
    """Our own Anonymous class to be able to call can method"""
    def can(self, persmission):
        return False


@login_manager.user_loader
def load_user(id:int):
    """Register user loader method for login manager"""
    return User.query.get(id)
