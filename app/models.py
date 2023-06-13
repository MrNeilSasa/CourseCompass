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
    name = db.Column(db.String(50), primary_key = True)

    def __init__(self, faculty, name):
        self.faculty = faculty
        self.name = name

    def __repr__(self):
        return '<Name %r>' % (self.name)    

class Course(db.Model):
    __tablename__ = 'courses'
    coursecode = db.Column(db.String(8), primary_key = True)
    coursename = db.Column(db.String(100))
    credithours = db.Column(db.Integer)
    semestersoffered = db.Column(db.String(50))
    prerequisites = db.Column(db.String(300))
    
    

    def __init__(self, coursecode, coursename, credithours, semestersoffered, prerequisites):
        self.coursecode = coursecode
        self.coursename = coursename
        self.credithours = credithours
        self.semestersoffered = semestersoffered
        self.prerequisites = prerequisites

    def __repr__(self):
        return '<coursecode %r>' % (self.coursecode)
    
class ExclusiveCourse(db.Model):
    __tablename__ = 'exclusivecourses'
    coursecode = db.Column(db.String(8), primary_key = True)
    coursename = db.Column(db.String(100))
    credithours = db.Column(db.Integer)
    semestersoffered = db.Column(db.String(50))
    prerequisites = db.Column(db.String(300))
    restriction = db.Column(db.String(200))
    
    

    def __init__(self, coursecode, coursename, credithours, semestersoffered, prerequisites, restriction):
        self.coursecode = coursecode
        self.coursename = coursename
        self.credithours = credithours
        self.semestersoffered = semestersoffered
        self.prerequisites = prerequisites
        self.restriction = restriction

    def __repr__(self):
        return '<coursecode %r>' % (self.coursecode)    


class CourseDescription(db.Model):
    __tablename__ = 'description'
    coursecode = db.Column(db.String(8), primary_key = True)
    coursedescription =  db.Column(db.String(5000))       
    prerequisites = db.Column(db.String(100))
    corequisites = db.Column(db.String(100))
    antirequisites = db.Column(db.String(100))

    def __init__(self, coursecode, coursedescription, prerequisites, corequisites, antirequisites):
        self.coursecode = coursecode
        self.coursedescription = coursedescription     
        self.prerequisites = prerequisites
        self.corequisites = corequisites
        self.antirequisites = antirequisites
    
    def __repr__(self):
        return '<Course Code %r>' % (self.coursecode)

class DifficultyRating(db.Model):
    __tablename__ = 'rating'
    coursecode = db.Column(db.String(8), primary_key = True)
    rating =  db.Column(db.Integer)

    def __init__(self, coursecode, rating):
        self.coursecode = coursecode
        self.rating = rating

    def __repr__(self):
        return '<Course Code %r>' % (self.coursecode)     
    
class DegreeOfferings(db.Model):
    __tablename__ = 'degrees'
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(50))
    degreename = db.Column(db.String(100))
    isoffered = db.Column(db.Boolean)
    yearoffered = db.Column(db.Integer)
    minnumofcredits = db.Column(db.Integer)
    
    def __init__(self, faculty, degreename, isoffered, minnumofcredits):
        self.faculty = faculty
        self.degreename = degreename
        self.isoffered = isoffered
        self.minnumofCredits = minnumofcredits

    def __repr__(self):
        return '<Degree %r>' % (self.degreeName)
    
class Qualifications(db.Model):
    __tablename__ = 'qualifications'
    id = db.Column(db.Integer, primary_key=True)
    qtype =  db.Column(db.String(50))
    subject = db.Column(db.String(50))

    def __init__(self, qtype, subject):
        self.qtype = qtype
        self.subject = subject
        

    def __repr__(self):
        return '<Type %r>' % (self.qtype)