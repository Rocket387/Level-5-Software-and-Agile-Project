from .extensions import db
from flask_login import UserMixin # class provides methods for flask_login such as is_authenticated 
#for example checking user is logged in before moving to home page)
from sqlalchemy.sql import func

#### Object Relational Mapping for database ####

#Class creates Note table to hold fields relating to notes made by users
#Note table includes Primary key (unique identifier) in the ID column
#and Foreign keys linking to user table and role table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(10000))
    date = db.Column(db.Date, default=func.current_date())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

   
    user = db.relationship('User', back_populates='notes') #user associated with a specific note
    role = db.relationship('Role', back_populates='notes') #role associated with a specific note

#Class creates table to hold fields relating to users
#User table includes Primary key in the ID column
#and Foreign key linking to role table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    alias = db.Column(db.String(150))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    
    role = db.relationship('Role', back_populates='users')
    notes = db.relationship('Note', back_populates='user', cascade="all, delete-orphan") #if user is deleted all related notes are deleted, and vice versa

    #function to check what trole the user has as this will determine whether they can delete notes or not (only if admin)
    def has_role(self, role_name):
        return self.role and self.role.roleName == role_name

#class creates table to hold fields relating to users roles (Admin or User)
#Role table includes Primary key in the ID column
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(150), unique=True)

    
    users = db.relationship('User', back_populates='role')
    notes = db.relationship('Note', back_populates='role')
