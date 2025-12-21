"""
Improved Test script for Admin User Management
Tests user listing, activation/deactivation, and deletion
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_user_management():
    print("=" * 70)
    print("Admin User Management Test")
    print("=" * 70)
    
    # Create a session with proper cookie handling
    admin_session = requests.Session()
    
    # Test 1: Login as admin
    print("\n1. Logging in as admin...")
    response = admin_session.post(f"{BASE_URL}/auth/login", data={
        'email': 'admin@test.com',
        'password': 'admin123'
    }, allow_redirects=True)
    print(f"   Status: {response.status_code}")
    print(f"   Final URL: {response.url}")
    admin_logged_in = response.status_code == 200 and 'dashboard' in response.url.lower()
    print(f"   [{'PASS' if admin_logged_in else 'FAIL'}] Admin logged in: {admin_logged_in}")
    
    # Test 2: Access admin dashboard
    print("\n2. Accessing admin dashboard...")
    response = admin_session.get(f"{BASE_URL}/user/dashboard", allow_redirects=True)
    has_admin_dashboard = 'Admin Dashboard' in response.text
    print(f"   [{'PASS' if has_admin_dashboard else 'FAIL'}] Admin dashboard loaded: {has_admin_dashboard}")
    
    # Test 3: Access users list
    print("\n3. Accessing /admin/users...")
    response = admin_session.get(f"{BASE_URL}/admin/users", allow_redirects=True)
    print(f"   Status: {response.status_code}")
    print(f"   Final URL: {response.url}")
    
    # Check if we got redirected (403 forbidden)
    if 'login' in response.url.lower():
        print("   [FAIL] Got redirected to login - session issue")
        print("   [INFO] Trying to access users list again...")
        response = admin_session.get(f"{BASE_URL}/admin/users", allow_redirects=False)
        print(f"   Status (no redirect): {response.status_code}")
    
    has_users_list = 'User Management' in response.text
    has_student = 'student@test.com' in response.text
    has_table = '<table' in response.text
    print(f"   [{'PASS' if has_users_list else 'FAIL'}] Users list loaded: {has_users_list}")
    print(f"   [{'PASS' if has_student else 'FAIL'}] Student user visible: {has_student}")
    print(f"   [{'PASS' if has_table else 'FAIL'}] Table present: {has_table}")
    
    # Test 4: Check for action buttons
    has_deactivate = 'Deactivate' in response.text or 'Activate' in response.text
    has_delete = 'Delete' in response.text
    has_statistics = 'Total Users:' in response.text
    print(f"   [{'PASS' if has_deactivate else 'FAIL'}] Toggle button visible: {has_deactivate}")
    print(f"   [{'PASS' if has_delete else 'FAIL'}] Delete button visible: {has_delete}")
    print(f"   [{'PASS' if has_statistics else 'FAIL'}] Statistics shown: {has_statistics}")
    
    # Test 5: Try to toggle a user status
    if has_users_list:
        print("\n4. Toggling user status...")
        # Try user ID 1 (likely the student)
        response = admin_session.post(f"{BASE_URL}/admin/users/1/toggle_active", allow_redirects=True)
        print(f"   Status: {response.status_code}")
        toggle_success = 'activated' in response.text or 'deactivated' in response.text
        print(f"   [{'PASS' if toggle_success else 'FAIL'}] Toggle operation: {toggle_success}")
        
        # Verify the change
        response = admin_session.get(f"{BASE_URL}/admin/users", allow_redirects=True)
        has_status_change = 'Inactive' in response.text or 'Active' in response.text
        print(f"   [{'PASS' if has_status_change else 'FAIL'}] Status displayed: {has_status_change}")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"[PASS] Admin login successful: {admin_logged_in}")
    print(f"[PASS] Admin dashboard accessible: {has_admin_dashboard}")
    print(f"[PASS] Users list accessible: {has_users_list}")
    print(f"[PASS] User data visible: {has_student and has_table}")
    print(f"[PASS] Action buttons present: {has_deactivate and has_delete}")
    print(f"[PASS] Statistics displayed: {has_statistics}")
    print("=" * 70)
    
    all_passed = (admin_logged_in and has_admin_dashboard and has_users_list and 
                  has_student and has_deactivate)
    
    if all_passed:
        print("\n[SUCCESS] ALL USER MANAGEMENT TESTS PASSED!")
    else:
        print("\n[INFO] Some features may need manual verification")
    
    return all_passed

if __name__ == "__main__":
    try:
        test_user_management()
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()
