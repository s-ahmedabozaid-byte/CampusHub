from run import app
from CampusHub.extensions import db

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
