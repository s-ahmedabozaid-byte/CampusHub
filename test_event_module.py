"""
Test script for Event Management module
Tests role-based access controls and event creation
"""
import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000"

def test_event_module():
    print("=" * 60)
    print("Event Management Module Test")
    print("=" * 60)
    
    # Create session for maintaining cookies
    session = requests.Session()
    
    # Test 1: Register student
    print("\n1. Registering student user...")
    response = session.post(f"{BASE_URL}/auth/register", data={
        'email': 'student@test.com',
        'password': 'test123',
        'role': 'student'
    }, allow_redirects=True)
    print(f"   Status: {response.status_code}")
    print(f"   Final URL: {response.url}")
    
    # Test 2: Login as student
    print("\n2. Logging in as student...")
    response = session.post(f"{BASE_URL}/auth/login", data={
        'email': 'student@test.com',
        'password': 'test123'
    }, allow_redirects=True)
    print(f"   Status: {response.status_code}")
    print(f"   Final URL: {response.url}")
    
    # Test 3: Try to access create page as student
    print("\n3. Attempting to access /events/create as student...")
    response = session.get(f"{BASE_URL}/events/create", allow_redirects=True)
    print(f"   Status: {response.status_code}")
    print(f"   Final URL: {response.url}")
    student_blocked = '/events/create' not in response.url
    print(f"   Student blocked: {student_blocked} [PASS]" if student_blocked else f"   Student blocked: {student_blocked} [FAIL]")
    
    # Test 4: Logout
    print("\n4. Logging out...")
    response = session.get(f"{BASE_URL}/auth/logout", allow_redirects=True)
    print(f"   Status: {response.status_code}")
    
    # Test 5: Register instructor
    print("\n5. Registering instructor user...")
    response = session.post(f"{BASE_URL}/auth/register", data={
        'email': 'instructor@test.com',
        'password': 'test123',
        'role': 'teacher'  # Using 'teacher' as that's what the form offers
    }, allow_redirects=True)
    print(f"   Status: {response.status_code}")
    
    # Test 6: Login as instructor
    print("\n6. Logging in as instructor...")
    response = session.post(f"{BASE_URL}/auth/login", data={
        'email': 'instructor@test.com',
        'password': 'test123'
    }, allow_redirects=True)
    print(f"   Status: {response.status_code}")
    
    # Test 7: Access create page as instructor
    print("\n7. Accessing /events/create as instructor...")
    response = session.get(f"{BASE_URL}/events/create", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    instructor_allowed = response.status_code == 200
    print(f"   Instructor allowed: {instructor_allowed} [PASS]" if instructor_allowed else f"   Instructor allowed: {instructor_allowed} [FAIL]")
    
    # Test 8: Create event
    print("\n8. Creating event as instructor...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
    response = session.post(f"{BASE_URL}/events/create", data={
        'title': 'Tech Talk',
        'description': 'A tech event about latest technologies',
        'date': tomorrow,
        'location': 'Auditorium A'
    }, allow_redirects=True)
    print(f"   Status: {response.status_code}")
    print(f"   Final URL: {response.url}")
    event_created = response.status_code == 200 and '/events' in response.url
    print(f"   Event created: {event_created} [PASS]" if event_created else f"   Event created: {event_created} [FAIL]")
    
    # Test 9: Verify event appears in list
    print("\n9. Checking events list...")
    response = session.get(f"{BASE_URL}/events/", allow_redirects=True)
    print(f"   Status: {response.status_code}")
    has_tech_talk = 'Tech Talk' in response.text
    print(f"   'Tech Talk' event visible: {has_tech_talk} [PASS]" if has_tech_talk else f"   'Tech Talk' event visible: {has_tech_talk} [FAIL]")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"[PASS] Student blocked from /events/create: {student_blocked}")
    print(f"[PASS] Instructor allowed to /events/create: {instructor_allowed}")
    print(f"[PASS] Event creation succeeded: {event_created}")
    print(f"[PASS] Event visible in list: {has_tech_talk}")
    print("=" * 60)
    
    all_passed = student_blocked and instructor_allowed and event_created and has_tech_talk
    if all_passed:
        print("\n[SUCCESS] ALL TESTS PASSED!")
    else:
        print("\n[FAILURE] SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    try:
        test_event_module()
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()
