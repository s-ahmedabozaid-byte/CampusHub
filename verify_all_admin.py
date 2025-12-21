import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from CampusHub.models.event_model import Event
from CampusHub.models.feedback_model import Feedback
from datetime import datetime

class TestAdminFeatures(unittest.TestCase):
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

    def test_feedback_flow(self):
        # Create user
        u = User(email='user@test.com', role='student')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        
        client = self.app.test_client()
        client.post('/auth/login', data={'email': 'user@test.com', 'password': 'password'}, follow_redirects=True)
        
        # Send Feedback
        response = client.post('/feedback/send', data={
            'category': 'Suggestion',
            'message': 'Great app!'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you for your feedback!', response.data)
        
        feedback = Feedback.query.first()
        self.assertIsNotNone(feedback)
        self.assertEqual(feedback.message, 'Great app!')
        print("Feedback submission verified.")

    def test_admin_dashboard_and_logs(self):
        # Create Admin
        admin = User(email='admin@test.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)
        
        # Create feedback to check stats
        # Need user for FK
        u = User(email='u2@test.com', role='student')
        db.session.add(u)
        db.session.commit()
        
        f = Feedback(user_id=u.id, message='Test Msg', category='Complaint')
        db.session.add(f)
        db.session.commit()

        client = self.app.test_client()
        client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'password'}, follow_redirects=True)
        
        # Check Dashboard
        response = client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total Feedbacks', response.data)
        self.assertIn(b'Test Msg', response.data)  # Check if message appears in list
        
        # Delete Feedback
        response = client.post(f'/admin/feedback/{f.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify deletion
        self.assertIsNone(Feedback.query.get(f.id))
        print("Admin dashboard and feedback deletion verified.")
        
        # Check Logs page
        response = client.get('/admin/logs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Activity Logs', response.data)
        print("Admin logs page verified.")

if __name__ == '__main__':
    unittest.main()
