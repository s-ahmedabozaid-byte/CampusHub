from werkzeug.security import generate_password_hash, check_password_hash

print("Testing check_password_hash with None hash...")
try:
    check_password_hash(None, "password")
    print("Success: None hash")
except Exception as e:
    print(f"Error: None hash -> {e}")

print("\nTesting check_password_hash with None password...")
try:
    check_password_hash("somehash", None)
    print("Success: None password")
except Exception as e:
    print(f"Error: None password -> {e}")

print("\nTesting generate_password_hash with None...")
try:
    generate_password_hash(None)
    print("Success: generate None")
except Exception as e:
    print(f"Error: generate None -> {e}")
