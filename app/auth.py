from flask import Blueprint
#authentication routes for web app

auth = Blueprint('auth', __name__)

#login route
@auth.route('/login')
def login():
    return 'Login'

#signup route
@auth.route('/signup')
def signup():
    return 'Signup'

#logout route
@auth.route('/logout')
def logout():
    return 'Logout'