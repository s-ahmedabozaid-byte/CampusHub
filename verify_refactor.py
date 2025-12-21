from CampusHub import create_app
from CampusHub.repositories.user_repository import UserRepository

app = create_app()

with app.app_context():
    print("App created successfully.")
    try:
        user_count = UserRepository.count()
        print(f"User count via Repository: {user_count}")
        print("Repository access successful.")
    except Exception as e:
        print(f"Error accessing Repository: {e}")
