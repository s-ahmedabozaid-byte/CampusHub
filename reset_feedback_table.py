from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.feedback_model import Feedback

app = create_app()
with app.app_context():
    # Dropping feedback table to reset schema
    Feedback.__table__.drop(db.engine)
    db.create_all()
    print("Feedback table reset successfully.")
