#importing required libraries and routes
from flask import Flask #adds Flask framework for URL routing and page rendering
from .extensions import db #imports SQL Alchemy from extensions, separate to prevent circular calls
from os import path #for local runs
from flask_login import LoginManager #handles users logging in and out sessions
from werkzeug.security import generate_password_hash #secure checks for passwords and hashing passwords
from .models import User, Role, Note #importing classes in models.py
from .config import Config #importing Config class in config.py
from datetime import datetime, timedelta #imports datetime for database entries

##### this file sets up the app #####



DB_NAME = 'PVWebAPPDB.db' #variable to name the database for web app

# function to create the web app, initializes database, create roles, admin and add notes
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app) #initializes app for use with database

    # Defines routes for web app
    from .views import views
    from .auth import auth

    #importing and registering the blueprint from the factory in views.py and auth.py
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note

    #setting up database and initializing it with the function calls
    with app.app_context():
        create_database(app)
        create_roles()
        create_admin_user()
        create_notes()

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #decorator ensures load_user function is used to retrieve user by ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #retrieves user id from database using SQLAlchemy

    return app

#function to create app database if it does not already exist
def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all()
        print('Created Database')
    else:
        print('Database already exits')

#function to create 2 roles, Admin or User
def create_roles():
    # Check if Admin and User roles already exist to avoid duplication
    if not Role.query.filter_by(roleName='Admin').first():
        admin = Role(roleName='Admin')
        db.session.add(admin)
    
    if not Role.query.filter_by(roleName='User').first():
        user = Role(roleName='User')
        db.session.add(user)
    
    db.session.commit()
    print("Roles created successfully!")

#function to assign Admin role to Admin
def create_admin_user():

    #assigns admin role to the admin user
    admin_role = Role.query.filter_by(roleName='Admin').first()

    #checks admin user exists
    if not User.query.filter_by(email='admin@example.com').first():
        admin_user = User(
            email='admin@example.com',
            alias='Admin',
            password=generate_password_hash('adminpass', method='pbkdf2:sha256'), #adding a salt and hashing password with shah256
            role=admin_role
        )
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created.')
    else:
        print('Admin user already exists.')

#Used this function to prepopulate the database with data and users
def create_notes():
    user_count = User.query.count()
    note_count = Note.query.count()

    # If there are already users or notes in the database, don't run this function
    if user_count > 0 or note_count > 0:
        print("Database already has users or notes, skipping note creation.")
        return 
    #creating sample users array
    users = []
    for i in range(1, 6): #creates 5 users
        email = f'user{i}@example.com'
        alias = f'User{i}'
        user = User.query.filter_by(email=email).first() #checks for users email in database
        if not user: #creates if does not already exist
            user = User(
                email=email,
                alias=alias,
                password=generate_password_hash('password', method='pbkdf2:sha256')
            )
            db.session.add(user) #adds user to database
            db.session.commit()
        users.append(user)
    
    #creates 10 notes by the 5 users with different dates
    for i in range(10):
        note_user = users[i % len(users)]
        note = Note(
            info=f'Note {i+1} by {note_user.alias}',
            date=datetime.utcnow() - timedelta(days=i),
            user_id=note_user.id
        )
        db.session.add(note)

    db.session.commit()
    print('Created 10 notes for different users.')