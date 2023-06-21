# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, SelectMultipleField, FloatField
from wtforms.validators import InputRequired, NumberRange
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField
from app import app, db
from app.models import Course, Faculty, Department, DegreeOfferings, Qualifications

class StudentForm(FlaskForm):
    yearOfStudy = IntegerField('Enter your current year of Study', validators=[InputRequired()])
    faculty = SelectField('Select your faculty', validators =[InputRequired()])
    department = SelectField('Select your faculty', validators =[InputRequired()])
    degree = SelectField('Select your Degree', validators=[InputRequired()])
    status = SelectField('Status', choices=[('full_time', 'Full Time'), ('part_time', 'Part Time')])
    startYear = IntegerField('Enter the year you started to your degree', validators=[InputRequired()])
    courses = SelectMultipleField('Select the courses you have completed/ currently taking', coerce=int)
    grades = StringField('Letter Grade:')
    gpa = FloatField('GPA', validators=[NumberRange(min=0, max=4.3)])
    desiredgpa = FloatField('Desired GPA', validators=[NumberRange(min=0, max=4.3)])
    exemptfrom = SelectMultipleField('Exepemted Courses', coerce=int)
    qualifications = SelectMultipleField('Select the type of qualifications you have obtained: ', coerce=int,
                                     choices=[('csec', 'CSEC'), ('cape', 'CAPE'), ('gce_a_level', 'GCE-A-Level'),('gce_o_level', 'GCE-O-Level'),
                                         ('associate_degree', 'Associate Degree'), ('teacher_associate_degree', 'Teacher Associate Degree'),
                                         ('sat', 'SAT')])
    qualSubject = SelectMultipleField('Select the type of prerequisite qualifications you have obtained: ', coerce=int,
                                  choices=[('accounting', 'Accounting'), ('applied_mathematics', 'Applied Mathematics'),
                                      ('biology', 'Biology'), ('business_studies', 'Business Studies'),
                                      ('caribbean_studies', 'Caribbean Studies'), ('chemistry', 'Chemistry'),
                                      ('communication_studies', 'Communication Studies'), ('computer_science', 'Computer Science'),
                                      ('economics', 'Economics'), ('english_language', 'English Language'), ('english_literature', 'English Literature'),
                                      ('environmental_science', 'Environmental Science'), ('french', 'French'),
                                      ('geography', 'Geography'), ('history', 'History'), ('information_technology', 'Information Technology'),
                                      ('law', 'Law'), ('literatures_in_english', 'Literatures in English'), ('mathematics', 'Mathematics'),
                                      ('physics', 'Physics'), ('principles_of_accounts', 'Principles of Accounts'),
                                      ('principles_of_business', 'Principles of Business'), ('psychology', 'Psychology'),
                                      ('pure_mathematics', 'Pure Mathematics'), ('reading_comprehension', 'Reading Comprehension'),
                                      ('social_studies', 'Social Studies'), ('sociology', 'Sociology'), ('spanish', 'Spanish'),
                                      ('writing_and_language', 'Writing and Language')])
    qualification_grades = SelectMultipleField('Qualification Grades:', choices=[('pass', 'Pass'), ('fail','Fail'), ('one', 'I'),
                                                                                ('two', 'II'), ('three', 'III'), ('four', 'IV'),
                                                                                ('five', 'V')])

def __init__(self, *args, **kwargs):
    super(StudentForm, self).__init__(*args, **kwargs)
    self.faculty.choices = [(faculty.faculty, faculty.faculty) for faculty in Faculty.query.all()]
    self.department.choices = [(department.name, department.name) for department in Department.query.all()]
    self.degree.choices = [(degree.degreename, degree.degreename) for degree in DegreeOfferings.query.all()]
    self.courses.choices = [(course.coursecode, course.coursecode) for course in Course.query.all()]
    self.exemptfrom.choices = [(course.coursecode, course.coursecode) for course in Course.query.all()]

    




class LoginForm(FlaskForm):
    email =  StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    email =  StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[InputRequired()])

