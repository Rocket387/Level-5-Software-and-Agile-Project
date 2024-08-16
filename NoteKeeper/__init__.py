#importing required libraries and routes
from flask import Flask
from .extensions import db
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .models import User, Role
from .config import Config

##### this file sets up the app #####



DB_NAME = 'PVWebAPPDB.db'

# function to create the web app, initializes database, create roles, admin and add notes
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Define routes here or in a separate file/module and import them
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note

    with app.app_context():
        create_database(app)
        create_roles()
        create_admin_user()
        create_notes()

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#fucntion to create app database
def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all()
        print('Created Database')
    else:
        print('Database already exits')

#fucntion to create 2 roles, Admin or User
def create_roles():
    # Check if roles already exist to avoid duplication
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

#fucntion to create notes, this ensures the database will always start with some data
#incase data added from the web app itself does not persist due to the web server Render
def create_notes():
    
    #creating sample users array
    users = []
    for i in range(1, 6): #creates 5 users
        email = f'user{i}@example.com'
        alias = f'User{i}'
        user = User.query.filter_by(email=email).first()
        if not user:
            email=email
            alias=alias
            password=generate_password_hash('password', method='pbkdf2:shah256')