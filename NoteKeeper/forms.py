
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


#### web app forms for user input ####
#Flask-WTF's has built-in Cross-Site Request Forgery protection. 
#CSRF token is added to forms and checks that the token matches form submissions,
#preventing malicious actions, Users are informed if they have entered data incorrectly
#in the corresponding field

#class creates fields for user to enter email and password in the login page
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#class creates fields for user to enter email, alias, password (+ comparison) in sign up page
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4)])
    alias = StringField('Alias', validators=[DataRequired(), Length(min=2)])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password2')])
    submit = SubmitField('Sign up')
