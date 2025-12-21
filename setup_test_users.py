from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.user_model import User

app = create_app()

with app.app_context():
    # Ensure admin user
    admin = User.query.filter_by(email='admin@test.com').first()
    if not admin:
        admin = User(email='admin@test.com', role='admin')
    admin.set_password('password123')
    admin.role = 'admin'
    admin.is_active = True
    db.session.add(admin)

    # Ensure student user
    student = User.query.filter_by(email='student@test.com').first()
    if not student:
        student = User(email='student@test.com', role='student')
    student.set_password('password123')
    student.role = 'student'
    student.is_active = True
    db.session.add(student)
    
    # Ensure another student user for deletion
    student2 = User.query.filter_by(email='todelete@test.com').first()
    if not student2:
        student2 = User(email='todelete@test.com', role='student')
    student2.set_password('password123')
    student2.role = 'student'
    student2.is_active = True
    db.session.add(student2)

    db.session.commit()
    print("Test users setup complete.")
