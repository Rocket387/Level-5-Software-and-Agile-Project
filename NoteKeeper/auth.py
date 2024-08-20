from flask import Blueprint, render_template, request, flash, redirect,url_for
from .models import User, Role
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, SignupForm


#### authentication routes for web app ####

#blueprint organizes related code for authentication
auth = Blueprint('auth', __name__)

#@auth.route decorator defines URL for and HTTP methods for login route
@auth.route('/login', methods=['GET', 'POST']) # POST to send/submit data, GET shows/requests data from server
def login():
    form = LoginForm() #creates an instance of the LoginFom

    #user enters email and password
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

    #checks users password and navigates to home page if correct data is entered
        user = User.query.filter_by(email=email).first() #SQLAlchemy querying method.
        if user and check_password_hash(user.password,password):
                flash('Logged in successfully', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
        else:
            #comment lets user know if they have entered their email or password incorrectly
            flash('Incorrect email or password, try again', category='error')

    #redirect to prevent resubmission issues
    return render_template('login.html', form=form)

#signup route
@auth.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm() #creates instanace of sign up form
    #User enters information to sign up to the note keeper
    if form.validate_on_submit():
        email = form.email.data
        alias = form.alias.data
        password1 = form.password1.data
        password2 = form.password2.data

        user=User.query.filter_by(email=email).first()

        #requirements for successful sign up, if user enters incorrect data a comment will flash up for them
        if user:
            flash('Email already exists',category='error')
        elif password1!=password2:
            flash('Passwords do not match',category='error')
        else:
            #new user is added to the database and password is hashed for security, user is directed to home page
            new_user = User(email=email,alias=alias,password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created',category='success')
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))
        
        #redirect to prevent resubmission issues
    return render_template("signup.html", form=form)

#logout route
@auth.route('/logout')
def logout():
    #Logs user out, user is shown successful logout comment and shown login page
    if login_user(current_user):
        logout_user()
        flash('Logged out successfully', category='success')
        return redirect(url_for('auth.login'))

