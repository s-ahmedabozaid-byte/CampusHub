from CampusHub.extensions import db

event_registrations = db.Table('event_registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('registration_date', db.DateTime, default=db.func.current_timestamp())
)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, default=3)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationship: Creator (One-to-Many)
    creator = db.relationship('User', backref=db.backref('created_events', lazy='dynamic'))
    
    # Relationship: Attendees (Many-to-Many)
    attendees = db.relationship('User', secondary=event_registrations, backref=db.backref('registered_events', lazy='dynamic'))

    @property
    def attendee_count(self):
        """Return the number of attendees."""
        return len(self.attendees)

    @property
    def is_full(self):
        """Check if the event has reached its maximum capacity."""
        if self.capacity is None:
            return False
        return self.attendee_count >= self.capacity

class Interest(db.Model):
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    
    # Unique constraint to prevent double liking
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='unique_user_event_interest'),)

    user = db.relationship('User', backref=db.backref('interests', lazy='dynamic'))
    event = db.relationship('Event', backref=db.backref('interests', lazy='dynamic'))

