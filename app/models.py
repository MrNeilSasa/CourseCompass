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
    courseCode = db.Column(db.String(8), primary_key = True)
    courseName = db.Column(db.String(100))
    creditHours = db.Column(db.Integer)
    semestersOffered = db.Column(db.String(50))
    prerequisites = db.Column(db.String(100))
    
    

    def __init__(self, courseCode, courseName, creditHours, semestersOffered, prerequisites):
        self.courseCode = courseCode
        self.courseName = courseName
        self.creditHours = creditHours
        self.semestersOffered = semestersOffered
        self.prerequisites = prerequisites

    def __repr__(self):
        return '<CourseCode %r>' % (self.courseCode)


class CourseDescription(db.Model):
    __tablename__ = 'description'
    courseCode = db.Column(db.String(8), primary_key = True)
    courseDescription =  db.Column(db.String(5000))       
    prerequisites = db.Column(db.String(100))
    corequisites = db.Column(db.String(100))
    antirequisites = db.Column(db.String(100))

    def __init__(self, courseCode, courseDescription, prerequisites, corequisites, antirequisites):
        self.courseCode = courseCode
        self.courseDescription = courseDescription     
        self.prerequisites = prerequisites
        self.corequisites = corequisites
        self.antirequisites = antirequisites
    
    def __repr__(self):
        return '<CourseCode %r>' % (self.courseCode)

class DifficultyRating(db.Model):
    __tablename__ = 'rating'
    courseCode = db.Column(db.String(8), primary_key = True)
    rating =  db.Column(db.Integer)

    def __init__(self, courseCode, rating):
        self.courseCode = courseCode
        self.rating = rating

    def __repr__(self):
        return '<CourseCode %r>' % (self.courseCode)     
    
class DegreeOfferings(db.Model):
    __tablename__ = 'degrees'
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(50))
    degreeName = db.Column(db.String(100))
    isOffered = db.Column(db.Boolean)
    minNumOfCredits = db.Column(db.Integer)
    
    def __init__(self, faculty, degreeName, isOffered, minNumOfCredits):
        self.faculty = faculty
        self.degreeName = degreeName
        self.isOffered = isOffered
        self.minNumOfCredits = minNumOfCredits

    def __repr__(self):
        return '<Degree %r>' % (self.degreeName)