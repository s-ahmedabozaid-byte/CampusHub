import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class TestEventList(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            user = User(email='test@example.com', role='student')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_event_list_render(self):
        # Login
        self.client.post('/auth/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        
        # Check events page
        response = self.client.get('/events/') # Assuming /events/ based on standard naming, will verify with grep result
        if response.status_code == 404:
             response = self.client.get('/events')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Events', response.data)

if __name__ == '__main__':
    unittest.main()
