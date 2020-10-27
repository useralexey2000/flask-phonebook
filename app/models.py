from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property


class Contact(db.Model):
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
    __tablename__ = 'phones'
    num = db.Column(db.Integer(), primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    def __repr__(self):
        return f'<Phone {self.num}>'
    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.num == other.num


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    # @hybrid_property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'<User {self.id}>'
