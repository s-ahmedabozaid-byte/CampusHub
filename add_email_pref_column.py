import sqlite3

def add_column():
    conn = sqlite3.connect('instance/campus_hub.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN receive_email_notifications BOOLEAN DEFAULT 1")
        conn.commit()
        print("Column 'receive_email_notifications' added successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error (column might already exist): {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_column()
