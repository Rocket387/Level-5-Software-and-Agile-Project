import unittest
from NoteKeeper import create_app, db
from NoteKeeper.models import User, Note, Role
from NoteKeeper.config import TestingConfig
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta #imports datetime for database entries


#### unit tests for webapp ####

class TestApp(unittest.TestCase):

    def setUp(self):

        #setting up testing config
        self.app = create_app(config_class=TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create database and add initial data
        db.create_all()

        # Check if the roles already exist before adding them
        self.admin_role = Role.query.filter_by(roleName='Admin').first()
        if not self.admin_role:
            self.admin_role = Role(roleName='Admin')
            db.session.add(self.admin_role)

        self.user_role = Role.query.filter_by(roleName='User').first()
        if not self.user_role:
            self.user_role = Role(roleName='User')
            db.session.add(self.user_role)

        self.admin_user = User(role=self.admin_role, email='admin@test.com', password=generate_password_hash('adminpass'))
        self.non_admin_user = User(role=self.user_role, email='user@test.com', password=generate_password_hash('userpass'))
        db.session.add(self.admin_user)
        db.session.add(self.non_admin_user)
        db.session.commit()


    def tearDown(self):
        #Removes database session and drops tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_login(self):
        #Test admin can log in
        with self.client as client:
            response = self.client.post('/login', data=dict(email='admin@test.com', password='adminpass'), follow_redirects=True)
            self.assertIn(b'Logged in successfully', response.data)
    
    def test_user_login(self):
        #Test admin can log in
        with self.client as client:
            response = self.client.post('/login', data=dict(email='user@test.com', password='userpass'), follow_redirects=True)
            self.assertIn(b'Logged in successfully', response.data)

    def test_user_incorrect_login(self):
        #Test admin can log in
        with self.client as client:
            response = self.client.post('/login', data=dict(email='user@test.com', password='test1abc'), follow_redirects=True)
            self.assertIn(b'Incorrect email or password, try again', response.data)

    def test_note_creation(self):
        #Test if admin can create a note
        self.client.post('/login', data=dict(email='admin@example.com', password='adminpass'), follow_redirects=True)
        response = self.client.post('/', data=dict(eventBox='Test Note'), follow_redirects=True)
        self.assertIn(b'Test Note', response.data)

    def test_user_signup(self):
        #Test user can sign up
        with self.client as client:
            response = self.client.post('/signup', data=dict(email='user1@example.com', alias='user1', password1='test1abc', password2= 'test1abc'), follow_redirects=True)
            self.assertIn(b'Account created', response.data)

    def test_user_signup_error(self):
        with self.client as client:
            response = self.client.post('/signup', data=dict(email='user1@example.com', alias='user1', password1='test1abc', password2= 'abc'), follow_redirects=True)
            self.assertIn(b'Passwords do not match', response.data)

    def test_user_logout(self):
        #Test user can logout
        with self.client as client:
            self.client.post('/login', data=dict(email='user@test.com', password='userpass'), follow_redirects=True)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'Logged out successfully', response.data)

### failing tests ###
    @unittest.expectedFailure
    def test_note_delete(self):
       with self.client as client:
            response = self.client.post('/login', data=dict(email='admin@test.com', password='adminpass'), follow_redirects=True)
            # Create a note to be deleted
            note = Note(info='Test Note for Deletion', role=self.admin_role.id)
            db.session.add(note)
            db.session.commit()

            response = self.client.delete(f'/delete-note/{note.id}', follow_redirects=True)
            self.assertIn(b'Note deleted successfully.', response.data)
            
    @unittest.expectedFailure
    def test_user_cannot_delete_note(self):
        with self.client as client:
            response = self.client.post('/login', data=dict(email='user@test.com', password='userpass'), follow_redirects=True)
            
            # Create a note to be deleted
            note = Note(info='Test Note for Deletion', role=self.user_role.id)
            db.session.add(note)
            db.session.commit()

            response = self.client.delete(f'/delete-note/{note.id}')
            self.assertIn(b'You do not have permission to delete this note.', response.data)

    @unittest.expectedFailure
    def test_note_edit(self):
       with self.client as client:
            response = self.client.post('/login', data=dict(email='user@test.com', password='userpass'), follow_redirects=True) 

        # Create a note to be edited
            note = Note(info='Test Note for Editing',
            date=datetime.utcnow(),
            user_id=1)
            db.session.add(note)
            db.session.commit()
            response = self.client.post('/edit-note/{note_user.1}')
            self.assertIn(b'Note successfully updated!', response.data)

    @unittest.expectedFailure
    def test_user_cannot_edit_note(self):
       with self.client as client:
            response = self.client.post('/login', data=dict(email='user@test.com', password='userpass'), follow_redirects=True)
            # Create a note to be edited
            response = self.client.post('/', data=dict(eventBox='Test Note for editing'), follow_redirects=True)
            self.assertIn(b'Test Note', response.data) 

            response = self.client.post('/', '/edit-note/2', data=dict(eventBox='Edited'), follow_redirects=True)
        
            self.assertIn(b'You do not have permission to edit this note!', response.data)

    @unittest.expectedFailure
    def test_user_has_added_more_than_1_character_edit_note(self):
       with self.client as client:
            response = self.client.post('/login', data=dict(email='user@test.com', password='userpass'), follow_redirects=True)
            # Create a note to be edited
            response = self.client.post('/', data=dict(eventBox='Test Note for editing', user_id = 3), follow_redirects=True)
            

            response = self.client.post('/', '/edit-note/{int:3}')
            self.assertIn(b'Note is too short', response.data)
    