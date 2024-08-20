import unittest
from NoteKeeper import create_app, db
from NoteKeeper.models import User, Note, Role
from NoteKeeper.config import TestingConfig

#### unit tests for webapp ####
### unsuccessful tests at the moment

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

        db.session.commit()

    def tearDown(self):
        #Removes database session and drops tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_login(self):
        #Test admin can log in
        response = self.client.post('/login', data=dict(email='admin@example.com', password='adminpass'), follow_redirects=True)
        self.assertIn(b'Logged in successfully', response.data)

    def test_note_creation(self):
        #Test if admin can create a note
        self.client.post('/login', data=dict(email='admin@example.com', password='adminpass'), follow_redirects=True)
        response = self.client.post('/', data=dict(eventBox='Test Note'), follow_redirects=True)
        self.assertIn(b'Test Note', response.data)

    def test_user_signup(self):
        #Test user can sign up
        response = self.client.post('/signup', data=dict(email='user1@example.com', alias='user1', password1='test1abc', password2= 'test1abc'), follow_redirects=True)
        self.assertIn(b'Account created', response.data)
       