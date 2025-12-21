from CampusHub.app import create_app
from CampusHub.extensions import db
from CampusHub.models.task_model import Task

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
    
    # Verify table existence
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables found: {tables}")
