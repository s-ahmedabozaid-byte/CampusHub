from run import app
from CampusHub.extensions import db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        try:
            # Add code column. SQLite 3.35+ supports DROP COLUMN but ADD COLUMN is supported long time.
            # UNIQUE constraint is hard to add via ALTER TABLE in SQLite. 
            # We will just add the column first.
            conn.execute(text("ALTER TABLE courses ADD COLUMN code VARCHAR(20)"))
            conn.commit()
            print("Column 'code' added successfully.")
            
            # Update existing records
            conn.execute(text("UPDATE courses SET code = 'CS' || CAST(id + 100 AS TEXT) WHERE code IS NULL"))
            conn.commit()
            print("Existing records updated.")
            
        except Exception as e:
            print(f"Error (maybe column exists): {e}")
