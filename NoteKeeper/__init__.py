#importing required libraries and routes
import sqlite3  # importing sqlite3 database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

##### this file sets up the app #####

# SQLAlchemy is a Python toolkit that simplifies database integration with web apps
db = SQLAlchemy()
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

    create_database(app)

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Databse')
