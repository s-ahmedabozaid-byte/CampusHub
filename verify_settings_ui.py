import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class TestSettingsAndUI(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create a test user
            user = User(email='test@example.com', role='student')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_settings_route(self):
        # Login first
        self.client.post('/auth/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        
        # Check settings page
        response = self.client.get('/user/settings')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Website Settings', response.data)

    def test_ui_classes(self):
        # Login to see sidebar
        self.client.post('/auth/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        
        response = self.client.get('/user/dashboard')
        self.assertEqual(response.status_code, 200)
        
        # Check for dark sidebar class
        self.assertIn(b'bg-gray-900', response.data)
        
        # Check for settings link
        self.assertIn(b'Settings', response.data)
        self.assertIn(b'/user/settings', response.data)
        
        # Check for transitions
        self.assertIn(b'transition-all', response.data)
        self.assertIn(b'duration-300', response.data)
        
        # Check main content background
        self.assertIn(b'bg-lamaSkyLight', response.data)

if __name__ == '__main__':
    unittest.main()
