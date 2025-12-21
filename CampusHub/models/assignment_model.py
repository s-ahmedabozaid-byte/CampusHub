from CampusHub.extensions import db
from datetime import datetime

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref=db.backref('assignments', lazy=True))

    @property
    def submissions_count(self):
        return 0 # Placeholder for now

    @property
    def average_score(self):
        return 0 # Placeholder for now
