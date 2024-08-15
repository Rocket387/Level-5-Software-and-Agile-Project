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

        #create database and add initial data
        db.create_all()

        # create roles
        self.admin_role = Role(roleName='Admin')
        self.user_role = Role(roleName='User')
        db.session.add(self.admin_role)
        db.session.add(self.user_role)
        db.session.commit()

        #create admin user
        self.admin_user = User(
            email='admin@example.com',
            alias='Admin',
            password='adminpass',
            role=self.admin_role
        )
        db.session.add(self.admin_user)
        db.session.commit()

    def tearDown(self):
        #Removes database session and drops tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_login(self):
        #Test admin can log in
        response = self.client.post('/login', data=dict(email='admin@example.com', password='adminpass'), follow_redirects=True)
        self.assertIn(b'Logged in succcessfully', response.data)

    def test_note_creation(self):
        #Test if admin can create a note
        self.client.post('/login', data=dict(email='admin@example.com', password='adminpass'), follow_redirects=True)
        response = self.client.post('/', data=dict(eventBox='Test Note'), follow_redirects=True)
        self.assertIn(b'Test Note', response.data)
