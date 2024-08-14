#importing required libraries and routes
import sqlite3  # importing sqlite3 database
from flask import Flask
from .extensions import db
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .models import User, Role

##### this file sets up the app #####

# SQLAlchemy is a Python toolkit that simplifies database integration with web apps

DB_NAME = 'PVWebAPPDB.db'

# function to create the web app, initializes database
def create_app():
    app = Flask(__name__)

    # securely generated secret key to manage sessions and protect against CSRF attacks
    app.config['SECRET_KEY'] = '85cab4e486a7bbaecbaea9420447fe59'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PVWebAppDB.db'
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

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all()
        print('Created Database')
    else:
        print('Database already exits')

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

def create_admin_user():

    # Assign admin role to the admin user
    admin_role = Role.query.filter_by(roleName='Admin').first()

    # Check if the admin user exists
    if not User.query.filter_by(email='admin@example.com').first():
        admin_user = User(
            email='admin@example.com',
            alias='Admin',
            password=generate_password_hash('adminpass', method='pbkdf2:sha256'),
            role=admin_role
        )
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created.')
    else:
        print('Admin user already exists.')

