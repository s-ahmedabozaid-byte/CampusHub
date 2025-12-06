import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create Student
            self.student = User(email='student@test.com', role='student')
            self.student.set_password('password')
            db.session.add(self.student)
            
            # Create Another User (for unique check)
            self.other = User(email='other@test.com', role='student')
            self.other.set_password('password')
            db.session.add(self.other)
            
            db.session.commit()
            self.student_id = self.student.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, email, password):
        return self.client.post('/auth/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_profile_access(self):
        self.login('student@test.com', 'password')
        response = self.client.get('/user/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Profile', response.data)
        self.assertIn(b'student@test.com', response.data)

    def test_update_email_success(self):
        self.login('student@test.com', 'password')
        response = self.client.post('/user/profile', data=dict(
            email='student_new@test.com'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile updated successfully!', response.data)
        self.assertIn(b'student_new@test.com', response.data)
        
        with self.app.app_context():
            user = User.query.get(self.student_id)
            self.assertEqual(user.email, 'student_new@test.com')

    def test_update_email_duplicate(self):
        self.login('student@test.com', 'password')
        response = self.client.post('/user/profile', data=dict(
            email='other@test.com'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email already registered.', response.data)
        
        with self.app.app_context():
            user = User.query.get(self.student_id)
            self.assertEqual(user.email, 'student@test.com')

if __name__ == '__main__':
    unittest.main()
