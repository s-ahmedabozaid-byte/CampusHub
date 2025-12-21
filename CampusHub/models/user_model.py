from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from CampusHub.extensions import db, login_manager
from .event_model import Event

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='student') # student, teacher, admin
    is_active = db.Column(db.Boolean, default=True)
    receive_email_notifications = db.Column(db.Boolean, default=True)
    
    # Relationship: Tasks (One-to-Many)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
