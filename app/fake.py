from faker import Faker
import random
from app import db
from sqlalchemy.exc import IntegrityError
from app.models import User, Contact, Phone

def users(count=10):
    """Create fake users for testing"""
    fake = Faker()
    i = 0
    while i < count:
        u = User(email = fake.email(), password = 'password')
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def contacts(count=100, phone_max=5, department_num=10):
    """Create fake contacts for testing"""
    fake = Faker()
    departments = ['department_'+ str(i) for i in range(department_num)]
    i = 0
    while i < count:
        phones = [ Phone(num = int(fake.msisdn())) for _ in range(random.randint(1, phone_max))]
        c = Contact(uname = fake.first_name(),
                    fname = fake.first_name(),
                    lname= fake.last_name(),
                    dep = departments[random.randint(0, department_num-1)],
                    pos = fake.job(),
                    phones = phones)
        db.session.add(c)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()