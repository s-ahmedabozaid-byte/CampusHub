import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class TestUIAndAdminReg(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_sidebar_visibility(self):
        # 1. Unauthenticated: Sidebar should NOT be present
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'<aside', response.data) # Sidebar tag should not be there
        self.assertIn(b'Admin Register', response.data) # Admin link should be there

        # 2. Authenticated: Sidebar SHOULD be present
        # Register and login
        self.client.post('/auth/register', data=dict(
            email='student@test.com',
            password='password',
            role='student'
        ), follow_redirects=True)
        
        self.client.post('/auth/login', data=dict(
            email='student@test.com',
            password='password'
        ), follow_redirects=True)
        
        response = self.client.get('/user/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<aside', response.data)

    def test_admin_registration_flow(self):
        # Test admin registration link and functionality
        response = self.client.get('/auth/register/admin')
        self.assertEqual(response.status_code, 200)
        
        # Register admin
        response = self.client.post('/auth/register/admin', data=dict(
            email='newadmin@test.com',
            password='password',
            secret_key='campusadmin'
        ), follow_redirects=True)
        
        self.assertIn(b'Admin registration successful', response.data)

if __name__ == '__main__':
    unittest.main()
