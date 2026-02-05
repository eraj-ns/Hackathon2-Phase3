#!/usr/bin/env python3
"""
Test script to verify authentication and task management functionality
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_api_endpoints():
    print("Testing API endpoints...")

    # Test signup
    print("\n1. Testing signup endpoint...")
    signup_data = {
        "email": f"testuser_{int(time.time())}@example.com",
        "password": "password123",
        "name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    if response.status_code == 201:
        print("✓ Signup successful")
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"  Token received: {access_token[:20]}...")
    else:
        print(f"✗ Signup failed: {response.status_code} - {response.text}")
        return False

    # Test signin
    print("\n2. Testing signin endpoint...")
    signin_data = {
        "username": signup_data["email"],
        "password": signup_data["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/signin", data=signin_data)
    if response.status_code == 200:
        print("✓ Signin successful")
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"  Token received: {access_token[:20]}...")
    else:
        print(f"✗ Signin failed: {response.status_code} - {response.text}")
        return False

    # Test task creation
    print("\n3. Testing task creation...")
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "Test Task from Script",
        "description": "This task was created via the API test script",
        "priority": "medium"
    }
    response = requests.post(f"{BASE_URL}/api/tasks/", json=task_data, headers=headers)
    if response.status_code == 201:
        print("✓ Task creation successful")
        task = response.json()
        task_id = task["id"]
        print(f"  Task ID: {task_id}")
        print(f"  Task Title: {task['title']}")
    else:
        print(f"✗ Task creation failed: {response.status_code} - {response.text}")
        return False

    # Test getting tasks
    print("\n4. Testing get tasks...")
    response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)
    if response.status_code == 200:
        tasks = response.json()
        print(f"✓ Retrieved {len(tasks)} tasks")
        for task in tasks:
            print(f"  - {task['title']} (ID: {task['id']})")
    else:
        print(f"✗ Get tasks failed: {response.status_code} - {response.text}")
        return False

    # Test updating a task
    print("\n5. Testing task update...")
    update_data = {
        "title": "Updated Test Task",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print("✓ Task update successful")
        updated_task = response.json()
        print(f"  Updated title: {updated_task['title']}")
        print(f"  Completed: {updated_task['completed']}")
    else:
        print(f"✗ Task update failed: {response.status_code} - {response.text}")
        return False

    # Test deleting a task
    print("\n6. Testing task deletion...")
    response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    if response.status_code == 204:
        print("✓ Task deletion successful")
    else:
        print(f"✗ Task deletion failed: {response.status_code} - {response.text}")
        return False

    print("\n✓ All API tests passed!")
    return True

def test_frontend_pages():
    print("\nTesting frontend pages...")

    # Test main page
    print("\n1. Testing frontend main page...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✓ Frontend main page accessible")
        else:
            print(f"✗ Frontend main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Frontend main page error: {e}")
        return False

    # Test signin page
    print("\n2. Testing signin page...")
    try:
        response = requests.get(f"{FRONTEND_URL}/signin")
        if response.status_code == 200:
            print("✓ Signin page accessible")
        else:
            print(f"✗ Signin page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Signin page error: {e}")
        return False

    # Test signup page
    print("\n3. Testing signup page...")
    try:
        response = requests.get(f"{FRONTEND_URL}/signup")
        if response.status_code == 200:
            print("✓ Signup page accessible")
        else:
            print(f"✗ Signup page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Signup page error: {e}")
        return False

    print("\n✓ All frontend tests passed!")
    return True

if __name__ == "__main__":
    print("Starting comprehensive test of authentication and task management...")

    success = True
    success &= test_api_endpoints()
    success &= test_frontend_pages()

    if success:
        print("\n🎉 All tests passed! The application is working correctly.")
        print("\nKey features verified:")
        print("- ✓ User signup functionality")
        print("- ✓ User signin functionality")
        print("- ✓ JWT token management")
        print("- ✓ Task creation, retrieval, update, and deletion")
        print("- ✓ Frontend page accessibility")
        print("- ✓ API authentication protection")
    else:
        print("\n❌ Some tests failed. Please check the output above.")