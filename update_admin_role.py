import sqlite3

conn = sqlite3.connect('instance/campushub.db')
cursor = conn.cursor()

# Update admin role
cursor.execute("UPDATE users SET role='admin' WHERE email='admin@test.com'")
conn.commit()

# Verify
cursor.execute("SELECT email, role FROM users WHERE email='admin@test.com'")
result = cursor.fetchone()

if result:
    print(f"Admin role updated successfully!")
    print(f"Email: {result[0]}, Role: {result[1]}")
else:
    print("Admin user not found")

conn.close()
