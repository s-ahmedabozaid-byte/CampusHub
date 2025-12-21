from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User
from CampusHub.models.course_model import Course
from CampusHub.models.event_model import Event, Interest
from CampusHub.models.review_model import Review
from datetime import datetime

app = create_app()

with app.app_context():
    # Setup
    db.create_all()
    
    # Create Instructor
    inst = User.query.filter_by(email='inst@test.com').first()
    if not inst:
        inst = User(email='inst@test.com', role='instructor')
        inst.set_password('pass')
        db.session.add(inst)
    
    # Create Student
    student = User.query.filter_by(email='stud@test.com').first()
    if not student:
        student = User(email='stud@test.com', role='student')
        student.set_password('pass')
        db.session.add(student)
    
    db.session.commit()
    
    print(f"Instructor ID: {inst.id}")
    print(f"Student ID: {student.id}")

    # 1. Create Course
    if not Course.query.filter_by(title='Python 101').first():
        c1 = Course(title='Python 101', description='Intro to Python', instructor_id=inst.id)
        db.session.add(c1)
        db.session.commit()
        print("Course 'Python 101' created.")
    else:
        c1 = Course.query.filter_by(title='Python 101').first()

    # 2. Enroll Student
    if c1 not in student.enrolled_courses:
        student.enrolled_courses.append(c1)
        db.session.commit()
        print(f"Student enrolled in {c1.title}.")
    else:
        print("Student already enrolled.")
        
    # 3. Event Like
    event = Event.query.first()
    if not event:
        # Create dummy event
        event = Event(title='Test Event', description='Desc', date=datetime.now(), location='Lab', creator_id=inst.id)
        db.session.add(event)
        db.session.commit()
        
    interest = Interest.query.filter_by(user_id=student.id, event_id=event.id).first()
    if not interest:
        i = Interest(user_id=student.id, event_id=event.id)
        db.session.add(i)
        db.session.commit()
        print("Student liked event.")
    
    # 4. Review
    # Event must be past ?? Logic in controller checks date.
    # Manually adding review to test model.
    review = Review(user_id=student.id, event_id=event.id, rating=5, comment="Great!")
    db.session.add(review)
    db.session.commit()
    print("Review added.")
    
    # Verification
    print(f"Course Enrollment Count: {c1.enrollment_count}")
    print(f"Event Likes: {event.interests.count()}")
    print(f"Event Reviews: {len(event.reviews)}")
