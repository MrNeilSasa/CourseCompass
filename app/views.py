"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, flash
import os
from app import app, db
import logging
from app.forms import StudentForm, LoginForm, RegisterForm
from app.models import Account, Student, Course, Faculty, Department, Qualifications
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from datetime import datetime, timedelta
from flask_cors import cross_origin
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})




@app.route('/api/v1/students/profile', methods=['POST'])
def create_profile():
    form = StudentForm(request.form)

    if form.validate():
        courses = ', '.join(form.courses.data)
        grades = ', '.join(form.grades.data)
        exemptfrom = ', '.join(form.exemptfrom.data)
        qualifications = ', '.join(form.qualifications.data)
        qualsubject = ', '.join(form.qualSubject.data)
        qualification_grades = ', '.join(form.qualification_grades.data)

        user_id = None  # Default value for users without an account

        if current_user.is_authenticated:
            user_id = current_user.id  # Get the user ID if the user is logged in

        profile = Student.query.filter_by(user_id=user_id).first()

        if profile:
            response_data = {
                'message': 'Profile already exists for the user.',
            }
            return jsonify(response_data), 409

        new_profile = Student(
            user_id=user_id,
            year_of_study=form.yearOfStudy.data,
            faculty=form.faculty.data,
            department=form.department.data,
            degree=form.degree.data,
            status=form.status.data,
            start_year=form.startYear.data,
            courses=courses,
            grades=grades,
            gpa=form.gpa.data,
            desired_gpa=form.desired_gpa.data,
            exemptfrom=exemptfrom,
            qualifications=qualifications,
            qualSubject=qualsubject,
            qualification_grades=qualification_grades
        )

        db.session.add(new_profile)
        db.session.commit()

        response_data = {
            'message': 'Student profile created successfully',
        }

        return jsonify(response_data)
    else:
        return jsonify(errors=form.errors)


@app.route('/api/v1/courses', methods=['GET'])
def get_courses():
    # Retrieve the list of courses from the database
    courses = Course.query.all()
    course_codes = [course.coursecode for course in courses]
    
    return jsonify(course_codes)

@app.route('/api/v1/faculty', methods=['GET'])
def get_faculties():
    # Retrieve the list of courses from the database
    faculties = Faculty.query.all()
    faculty_name = [faculty.faculty for faculty in faculties]
    
    return jsonify(faculty_name)

@app.route('/api/v1/departments', methods=['GET'])
def getDepartments():
    departments = Department.query.all()
    department_list = [department.name for department in departments]
    return jsonify(department_list)    

@app.route('/api/v1/grades', methods=['GET'])
def get_grades():
    # Retrieve the list of grades from the database
    grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'F1', 'F2', 'F3', 'FE/FC', 
             'FE1/FC1',  'FE2/FC2', 'FE3/FC3'] 
    
    return jsonify(grades)

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    # Retrieve the list of grades from the database
    status = ['Full Time', 'Part Time'] 
    
    return jsonify(status)

@app.route('/api/v1/qualifications', methods=['GET'])
def get_qualifications():
    # Retrieve the list of qualifications from the database
    qualification_types = ['CSEC', 'CAPE', 'GCE-A-Level', 'GCE-O-Level', 'Associate Degree', 'Teacher Associate Degree',
                           'SAT']
    return jsonify(qualification_types)

@app.route('/api/v1/qualsubjects', methods=['GET'])
def get_qualsubjects():
    # Retrieve the list of qualification subjects from the database
    qualifications = Qualifications.query.all()
    qualification_subjects = ['Accounting', 'Applied Mathematics', 'Biology', 'Business Studies', 'Caribbean Studies',
                            'Chemistry', 'Communication Studies', 'Computer Science', 'Economics', 'English Language',
                            'English Literature', 'Environmental Science', 'French', 'Geography', 'History',
                            'Information Technology', 'Law', 'Literatures in English', 'Mathematics', 'Physics',
                            'Principles of Accounts', 'Principles of Business', 'Psychology', 'Pure Mathematics',
                            'Reading Comprehension', 'Social Studies', 'Sociology', 'Spanish', 'Writing and Language']
    
    return jsonify(qualification_subjects)

@app.route('/api/v1/qualgrades', methods=['GET'])
def get_qualgrades():
    qualgrades = ['Pass', 'Fail', 'I', 'II', 'III', 'IV', 'V']  

    return jsonify(qualgrades)



@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirmpassword = form.confirmpassword.data
        if confirmpassword == password:
            user = Account(email, password)
            db.session.add(user)
            db.session.commit()

            message = 'Your account has been created!'
            response = {
                'message': message,
                'email': email,
                'password': password,
                'confirmpassword': password,
            }
            return jsonify(response), 201
    else:
        errors = form_errors(form)
        response = {'errors': errors}
        return jsonify(response)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Account.query.filter_by(email=email).first()

        if user is not None and check_password_hash(user.password, password):
            login_user(user)

            response_data = {
                'message': 'Logged in successfully.'
            }

            flash('Logged in successfully.', 'success')

        else:
            response_data = {
                'message': 'Email or password is incorrect.'
            }
            flash('Email or password is incorrect.', 'danger')

        return jsonify(response_data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    response_data = {
        'message': 'Logged out successfully.'
    }
    return jsonify(response_data)



###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404