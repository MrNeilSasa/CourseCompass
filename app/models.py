# Add any model classes for Flask-SQLAlchemy here
from datetime import datetime
from . import db
import random
from werkzeug.security import generate_password_hash

class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.String(8), primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(500))

    def __init__(self, email, password):
        self.id = self.generate_unique_id()
        self.email = email
        self.password = generate_password_hash(password)
        

    def generate_unique_id(self):
        used_ids = set(Account.query.with_entities(Account.id).all())
        while True:
            unique_id = str(random.randint(10000000, 99999999))
            if unique_id not in used_ids:
                return unique_id
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Email %r>' % (self.email)           

class Faculty(db.Model):
    __tablename__ = "faculties"
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(50), unique=True)


    def __init__(self, faculty):
        self.faculty = faculty
    def __repr__(self):
        return '<Faculty %r>' % (self.faculty) 

class Department(db.Model):
    __tablename__ = 'department'
    faculty = db.Column(db.String(50))
    name = db.Column(db.String(50), unique=True)

    def __init__(self, faculty, name):
        self.faculty = faculty
        self.name = name

    def __repr__(self):
        return '<Name %r>' % (self.name)    

