from flask import Blueprint, request, jsonify, session
from .models import User, Role
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, current_user
import re

auth = Blueprint('auth', __name__)

def contains_invalid_chars(value):
    invalid_chars = re.compile(r"[<>/\"'`;]")
    return bool(invalid_chars.search(value))

def is_valid_email(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return email_pattern.match(email)

@auth.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate for malicious characters
    if contains_invalid_chars(email):
        return jsonify({'error': 'Invalid characters detected. Please remove any of the following: <, >, ", \', `, ;'}), 400


    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        print("Stored hash in DB:", user.password, flush=True)  
        print("Password check:", check_password_hash(user.password, password)) 

    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Incorrect email or password. Please try again.'}), 401

@auth.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    alias = data.get('alias')
    password1 = data.get('password1')
    password2 = data.get('password2')

    if not email or not alias or not password1 or not password2:
        return jsonify({'error': 'All fields are required.'}), 400
    
    if contains_invalid_chars(email):
        return jsonify({'error': 'Invalid characters detected. Please remove any of the following: <, >, ", \', `, ;'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'Email already exists.'}), 400
    elif password1 != password2:
        return jsonify({'error': 'Passwords do not match.'}), 400
    else:
        user_role = Role.query.filter_by(roleName='User').first()
        new_user = User(
            email=email,
            alias=alias,
            password=generate_password_hash(password1, method='pbkdf2:sha256'),
            role_id=user_role.id
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return jsonify({'message': 'Account created successfully.'}), 201

@auth.route('/api/auth/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        session.clear()
        return jsonify({'message': 'Logged out successfully.'}), 200
    else:
        return jsonify({'error': 'No user is currently logged in.'}), 401
