from .extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#### Object Relational Mapping for database ####

#Class creates Note table to hold fields relating to notes made by users
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(10000))
    date = db.Column(db.Date, default=func.current_date())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # Define relationship back to user and role
    user = db.relationship('User', back_populates='notes')
    role = db.relationship('Role', back_populates='notes')

#Class creates table to hold fields relating to users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    alias = db.Column(db.String(150))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # Define relationship back to role and note
    role = db.relationship('Role', back_populates='users')
    notes = db.relationship('Note', back_populates='user', cascade="all, delete-orphan")

    #function to check what trole the user has as this will determine whether they can delete notes or not (only if admin)
    def has_role(self, role_name):
        return self.role and self.role.roleName == role_name

#class creates table to hold fields relating to users roles (Admin or User)
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(150), unique=True)

    # Define relationship back to users and notes
    users = db.relationship('User', back_populates='role')
    notes = db.relationship('Note', back_populates='role')
