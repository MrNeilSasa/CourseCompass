# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import InputRequired
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField

class LoginForm(FlaskForm):
    email =  StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    email =  StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[InputRequired()])

