import unittest
from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from CampusHub.models.event_model import Event
from CampusHub.models.task_model import Task
from datetime import datetime

class TestCapacityAndTasks(unittest.TestCase):
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

    def test_task_routes(self):
        # Create user
        u = User(email='task_user@test.com', role='student')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        
        client = self.app.test_client()
        
        # Login
        client.post('/auth/login', data={'email': 'task_user@test.com', 'password': 'password'}, follow_redirects=True)
        
        # Create Task
        response = client.post('/tasks/create', data={
            'title': 'New Task',
            'description': 'Task Desc',
            'deadline': '2025-12-31T23:59'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Task', response.data)
        
        # Verify in DB
        task = Task.query.first()
        self.assertIsNotNone(task)
        self.assertEqual(task.title, 'New Task')
        self.assertEqual(task.status, 'Pending')
        
        # Toggle Task
        response = client.post(f'/tasks/{task.id}/toggle', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        db.session.refresh(task)
        self.assertEqual(task.status, 'Completed')
        
        # Toggle back
        client.post(f'/tasks/{task.id}/toggle', follow_redirects=True)
        db.session.refresh(task)
        self.assertEqual(task.status, 'Pending')
        
        print("Task routes (create, list, toggle) verified.")

if __name__ == '__main__':
    unittest.main()
