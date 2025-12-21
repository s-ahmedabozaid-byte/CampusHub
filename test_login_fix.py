"""
Quick test to verify login works after is_active fix
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

session = requests.Session()

# Test login
print("Testing login with admin@test.com...")
response = session.post(f"{BASE_URL}/auth/login", data={
    'email': 'admin@test.com',
    'password': 'admin123'
}, allow_redirects=True)

print(f"Status: {response.status_code}")
print(f"Final URL: {response.url}")
print(f"Login successful: {'dashboard' in response.url or 'Dashboard' in response.text}")

# Try accessing dashboard
response = session.get(f"{BASE_URL}/user/dashboard", allow_redirects=True)
print(f"\nDashboard access:")
print(f"Status: {response.status_code}")
print(f"Has 'Admin Dashboard': {'Admin Dashboard' in response.text}")
print(f"Has 'Welcome': {'Welcome' in response.text}")

# Try accessing users list
response = session.get(f"{BASE_URL}/admin/users", allow_redirects=True)
print(f"\nUsers list access:")
print(f"Status: {response.status_code}")
print(f"Has 'User Management': {'User Management' in response.text}")
print(f"Has user table: {'<table' in response.text}")
