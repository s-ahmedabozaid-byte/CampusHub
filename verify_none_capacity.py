import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from CampusHub.models.event_model import Event
from datetime import datetime

class TestNoneCapacity(unittest.TestCase):
    def setUp(self):
        class Config:
            TESTING = True
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
            WTF_CSRF_ENABLED = False
            SECRET_KEY = 'test'

        self.app = create_app(Config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_page_render_with_none_capacity(self):
        # Create user and event with None capacity
        u1 = User(email='u1@test.com', role='student')
        creator = User(email='creator@test.com', role='teacher')
        
        event = Event(
            title='Test Event None Cap',
            description='Desc',
            date=datetime.now(),
            location='Room 1',
            capacity=None,
            creator=creator,
            is_approved=True
        )
        db.session.add_all([u1, creator, event])
        db.session.commit()

        # Render list page
        client = self.app.test_client()
        with client:
            client.post('/auth/login', data={'email': 'u1@test.com', 'password': ''}, follow_redirects=True)
            # Login manual simulation if needed or skip since login required
            # Actually, need to set password for u1 to login
            u1.set_password('password')
            db.session.commit()
            
            client.post('/auth/login', data={'email': 'u1@test.com', 'password': 'password'}, follow_redirects=True)
            response = client.get('/events/')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Open Event', response.data)
            print("Page rendered successfully with None capacity event.")

if __name__ == '__main__':
    unittest.main()
