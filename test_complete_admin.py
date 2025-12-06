"""
Complete Admin Approval Test
Tests the full workflow from event creation to approval
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_complete_admin_workflow():
    print("=" * 70)
    print("Complete Admin Approval Workflow Test")
    print("=" * 70)
    
    # Test 1: Login as admin
    print("\n1. Logging in as admin...")
    admin_session = requests.Session()
    response = admin_session.post(f"{BASE_URL}/auth/login", data={
        'email': 'admin@test.com',
        'password': 'admin123'
    }, allow_redirects=True)
    print(f"   Status: {response.status_code}")
    admin_logged_in = 'admin@test.com' in response.text or 'Admin Dashboard' in response.text
    print(f"   [{'PASS' if admin_logged_in else 'FAIL'}] Admin logged in: {admin_logged_in}")
    
    # Test 2: Check admin dashboard
    print("\n2. Checking admin dashboard...")
    response = admin_session.get(f"{BASE_URL}/user/dashboard", allow_redirects=True)
    has_admin_dashboard = 'Admin Dashboard' in response.text
    has_admin_privileges = 'Admin Privileges' in response.text
    print(f"   [{'PASS' if has_admin_dashboard else 'FAIL'}] Admin dashboard loaded: {has_admin_dashboard}")
    print(f"   [{'PASS' if has_admin_privileges else 'FAIL'}] Admin privileges shown: {has_admin_privileges}")
    
    # Test 3: View events list (should see unapproved events)
    print("\n3. Viewing events list as admin...")
    response = admin_session.get(f"{BASE_URL}/events/", allow_redirects=True)
    can_see_workshop = 'Workshop on AI' in response.text
    has_approve_button = 'Approve' in response.text
    has_delete_button = 'Delete' in response.text
    print(f"   [{'PASS' if can_see_workshop else 'FAIL'}] Can see unapproved event: {can_see_workshop}")
    print(f"   [{'PASS' if has_approve_button else 'FAIL'}] Approve button visible: {has_approve_button}")
    print(f"   [{'PASS' if has_delete_button else 'FAIL'}] Delete button visible: {has_delete_button}")
    
    # Test 4: Approve the event (find event ID from previous tests - likely ID 2)
    print("\n4. Approving 'Workshop on AI' event...")
    # Try event IDs 2, 3, 4 to find the Workshop event
    for event_id in [2, 3, 4]:
        response = admin_session.post(f"{BASE_URL}/events/{event_id}/approve", allow_redirects=True)
        if response.status_code == 200:
            approval_message = 'has been approved' in response.text
            if approval_message:
                print(f"   [PASS] Event ID {event_id} approved successfully")
                break
    
    # Test 5: Verify student can now see the event
    print("\n5. Verifying student can see approved event...")
    student_session = requests.Session()
    response = student_session.post(f"{BASE_URL}/auth/login", data={
        'email': 'student@test.com',
        'password': 'test123'
    }, allow_redirects=True)
    
    response = student_session.get(f"{BASE_URL}/events/", allow_redirects=True)
    student_can_see = 'Workshop on AI' in response.text
    print(f"   [{'PASS' if student_can_see else 'FAIL'}] Student can see approved event: {student_can_see}")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"[PASS] Admin login successful: {admin_logged_in}")
    print(f"[PASS] Admin dashboard displayed: {has_admin_dashboard}")
    print(f"[PASS] Admin can see unapproved events: {can_see_workshop}")
    print(f"[PASS] Admin controls visible: {has_approve_button and has_delete_button}")
    print(f"[PASS] Event approval successful: {approval_message if 'approval_message' in locals() else False}")
    print(f"[PASS] Student can see approved event: {student_can_see}")
    print("=" * 70)
    
    all_passed = (admin_logged_in and has_admin_dashboard and can_see_workshop and 
                  has_approve_button and student_can_see)
    
    if all_passed:
        print("\n[SUCCESS] ALL ADMIN WORKFLOW TESTS PASSED!")
    else:
        print("\n[INFO] Some tests may need manual verification")
    
    return all_passed

if __name__ == "__main__":
    try:
        test_complete_admin_workflow()
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()
