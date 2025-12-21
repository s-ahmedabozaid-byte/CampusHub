import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from CampusHub.models.task_model import Task
from CampusHub.models.event_model import Event
from CampusHub.models.feedback_model import Feedback

class TestReportsAndSettings(unittest.TestCase):
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

    def test_admin_reports(self):
        # Setup Data
        admin = User(email='admin@reports.com', role='admin')
        admin.set_password('pass')
        db.session.add(admin)
        
        # Add task for efficiency stat
        t = Task(title='T1', status='Completed', user=admin)
        db.session.add(t)
        
        # Add feedback
        f = Feedback(message='F1', category='Bug', user=admin)
        db.session.add(f)
        
        db.session.commit()
        
        client = self.app.test_client()
        client.post('/auth/login', data={'email': 'admin@reports.com', 'password': 'pass'})
        
        response = client.get('/admin/reports')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'System Reports', response.data)
        # Check stat values roughly
        self.assertIn(b'100.0%', response.data) # 1/1 tasks completed
        
        print("Admin Reports Verified.")

    def test_user_settings(self):
        u = User(email='user@settings.com', role='student')
        u.set_password('oldpass')
        db.session.add(u)
        db.session.commit()
        
        client = self.app.test_client()
        client.post('/auth/login', data={'email': 'user@settings.com', 'password': 'oldpass'})
        
        # 1. Update Profile
        client.post('/user/settings', data={
            'action': 'update_profile',
            'email': 'new@settings.com',
            'username': 'NewUser'
        }, follow_redirects=True)
        
        u = User.query.get(u.id)
        self.assertEqual(u.email, 'new@settings.com')
        self.assertEqual(u.username, 'NewUser')
        
        # 2. Change Password
        client.post('/user/settings', data={
            'action': 'change_password',
            'password': 'newpass'
        }, follow_redirects=True)
        
        self.assertTrue(u.check_password('newpass'))
        
        # 3. Preferences
        client.post('/user/settings', data={
            'action': 'update_preferences',
            'receive_email_notifications': 'true'
        }, follow_redirects=True)
        u = User.query.get(u.id)
        self.assertTrue(u.receive_email_notifications)
        
        # Toggle off
        client.post('/user/settings', data={
            'action': 'update_preferences'
            # No checkbox sent means False usually in HTML forms, but logic: request.form.get() == 'true'
            # If unticked, it's missing or 'false'? 
            # In HTML unchecked checkboxes are not sent. My logic: get(...) == 'true'. So if missing -> False. Correct.
        }, follow_redirects=True)
        u = User.query.get(u.id)
        self.assertFalse(u.receive_email_notifications)
        
        print("User Settings Verified.")

if __name__ == '__main__':
    unittest.main()
