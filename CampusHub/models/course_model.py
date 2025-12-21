from CampusHub.extensions import db

enrollments = db.Table('enrollments',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('enrollment_date', db.DateTime, default=db.func.current_timestamp())
)

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    instructor = db.relationship('User', backref=db.backref('courses_taught', lazy=True))
    students = db.relationship('User', secondary=enrollments, backref=db.backref('enrolled_courses', lazy='dynamic'))

    code = db.Column(db.String(20), unique=True, default='TBD') # Added default for migration

    @property
    def enrollment_count(self):
        return len(self.students)

    @property
    def status(self):
        return "Active"

    @property
    def assignments_count(self):
        return len(self.assignments) if self.assignments else 0

    @property
    def materials_count(self):
        return 0 # Placeholder until Materials model exists
