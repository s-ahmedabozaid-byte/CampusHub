from CampusHub.models.user_model import User
from flask import Flask

app = Flask(__name__)

with app.app_context():
    u = User()
    u.password_hash = None
    
    print("Testing check_password(None) with None hash...")
    try:
        res = u.check_password(None)
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")

    print("\nTesting check_password('password') with None hash...")
    try:
        res = u.check_password('password')
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")

    u.set_password('validpassword')
    print("\nTesting check_password(None) with Valid hash...")
    try:
        res = u.check_password(None)
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")
