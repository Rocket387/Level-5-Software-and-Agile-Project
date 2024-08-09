from flask import Blueprint, render_template, request, flash, redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#### authentication routes for web app ####

auth = Blueprint('auth', __name__)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully', category='success')
                login_user(user,remember=False)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', category='error')

#signup route
@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',catergory='error')
        elif len(email)<4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstName)<2:
            flash('First nme must be greater than 1 character',category='error')
        elif password1!=password2:
            flash('Passwords do not match',category='error')
        elif len(password1)<7:
            flash('Password must be greater than 6 characters',category='error')
        else:
            new_user = User(email=email,firstName=firstName,password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created',category='success')
            login_user(user,remember=False)
            return redirect(url_for('views.home'))
        
    return render_template("signup.html",user=current_user)

#logout route
@auth.route('/logout')
def logout():
    if login_user(current_user):
        flash('Logged out successfully', category='success')

    return redirect(url_for('auth.login'))