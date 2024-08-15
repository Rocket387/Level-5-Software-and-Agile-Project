from flask import Blueprint, render_template, request, flash, redirect,url_for
from .models import User, Role
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#### authentication routes for web app ####

auth = Blueprint('auth', __name__)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    #user enters email and password
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

    #checks users password and navigates to home page if correct data is entered
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                #comment lets user know if they have entered their password incorrectly
                flash('Incorrect password, try again', category='error')
        else:
            #comment lets user know their email does not exist and they need to sign up
            flash('Email does not exist. Please sign up first', category='error')
    
    #redirect to prevent resubmission issues
    return render_template('login.html', category='error')

#signup route
@auth.route('/signup',methods=['GET','POST'])
def signup():
    #User enters information to sign up to the note keeper
    if request.method=='POST':
        email=request.form.get('email')
        alias=request.form.get('alias')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()

        #requirements for successful sign up, if user enters incorrect data a comment will flash up for them
        if user:
            flash('Email already exists',category='error')
        elif len(email)<4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(alias)<2:
            flash('alias must be greater than 1 character',category='error')
        elif password1!=password2:
            flash('Passwords do not match',category='error')
        elif len(password1)<7:
            flash('Password must be greater than 6 characters',category='error')
        else:
            #new user is added to the database and password is hashed for security, user is directed to home page
            new_user = User(email=email,alias=alias,password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created',category='success')
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))
        
        #redirect to prevent resubmission issues
    return render_template("signup.html",user=current_user)

#logout route
@auth.route('/logout')
def logout():
    #Logs user out, user is shown successful logout comment and shown login page
    if login_user(current_user):
        logout_user()
        flash('Logged out successfully', category='success')
        return redirect(url_for('auth.login'))