import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class TestRegisterPage(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_page_renders(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Account', response.data)
        self.assertIn(b'Admin Register', response.data)

    def test_register_student(self):
        response = self.client.post('/auth/register', data=dict(
            email='student@test.com',
            password='password',
            role='student'
        ), follow_redirects=True)
        
        self.assertIn(b'Registration successful', response.data)
        
        with self.app.app_context():
            user = User.query.filter_by(email='student@test.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.role, 'student')

    def test_register_teacher(self):
        response = self.client.post('/auth/register', data=dict(
            email='teacher@test.com',
            password='password',
            role='teacher'
        ), follow_redirects=True)
        
        self.assertIn(b'Registration successful', response.data)
        
        with self.app.app_context():
            user = User.query.filter_by(email='teacher@test.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.role, 'teacher')

if __name__ == '__main__':
    unittest.main()
