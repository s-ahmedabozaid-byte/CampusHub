import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class TestProfileUpdate(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            user = User(email='student@test.com', role='student')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_profile_page_renders(self):
        # Login
        self.client.post('/auth/login', data=dict(
            email='student@test.com',
            password='password'
        ), follow_redirects=True)
        
        # Access profile page
        response = self.client.get('/user/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Profile', response.data)
        self.assertIn(b'student@test.com', response.data)

    def test_profile_update_email(self):
        # Login
        self.client.post('/auth/login', data=dict(
            email='student@test.com',
            password='password'
        ), follow_redirects=True)
        
        # Update profile
        response = self.client.post('/user/profile', data=dict(
            email='student_new@test.com',
            username='TestStudent'
        ), follow_redirects=True)
        
        self.assertIn(b'Profile updated successfully!', response.data)
        
        # Verify update in database
        with self.app.app_context():
            user = User.query.filter_by(email='student_new@test.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'TestStudent')

    def test_profile_duplicate_email(self):
        # Create another user
        with self.app.app_context():
            user2 = User(email='another@test.com', role='student')
            user2.set_password('password')
            db.session.add(user2)
            db.session.commit()
        
        # Login as first user
        self.client.post('/auth/login', data=dict(
            email='student@test.com',
            password='password'
        ), follow_redirects=True)
        
        # Try to update to existing email
        response = self.client.post('/user/profile', data=dict(
            email='another@test.com'
        ), follow_redirects=True)
        
        self.assertIn(b'Email already registered', response.data)

if __name__ == '__main__':
    unittest.main()
