#importing required libraries and routes
import sqlite3  # importing sqlite3 database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# this file sets up the app

# SQLAlchemy is a Python toolkit that simplifies database integration with web apps
db = SQLAlchemy()

# function to create the web app, initializes database
def create_app():
    app = Flask(__name__)

    # securely generated secret key to manage sessions and protect against CSRF attacks
    app.config['SECRET_KEY'] = 'ENTER YOUR SECRET KEY HERE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PVWebAppDB.db'

    db.init_app(app)

    # Define routes here or in a separate file/module and import them

    # checks connection to PVWebApp Database
    @app.route('/')
    def testdb():
        try:
            # db.session.execute('SELECT 1')
            db.session.execute(text('SELECT 1'))
            return 'Connection successful!'
        except Exception as e:
            return f'Connection failed! ERROR: {e}'

    return app

if __name__ == '__main__':
    app = create_app()  # Create the app instance
    app.run(debug=True)

testdb should not be a route, it should be included in the web app once the user has logged in to let the user know they have connected to the database successfully
