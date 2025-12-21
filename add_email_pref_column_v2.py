from CampusHub.app import create_app
from CampusHub.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN receive_email_notifications BOOLEAN DEFAULT 1"))
            conn.commit()
        print("Column 'receive_email_notifications' added successfully.")
    except Exception as e:
        print(f"Error (column might already exist): {e}")
