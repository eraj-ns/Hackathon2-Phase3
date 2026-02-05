import requests
import json

# Test the new API endpoints with advanced features
BASE_URL = "http://localhost:8000"

# Test signup
print("Testing signup...")
signup_response = requests.post(f"{BASE_URL}/auth/signup", json={
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
})

print(f"Signup status: {signup_response.status_code}")
if signup_response.status_code == 200:
    auth_data = signup_response.json()
    token = auth_data.get('access_token')
    print("Signup successful!")
else:
    print(f"Signup failed: {signup_response.text}")
    # Try signing in if user already exists
    signin_response = requests.post(f"{BASE_URL}/auth/signin", data={
        "username": "test@example.com",
        "password": "password123"
    })
    if signin_response.status_code == 200:
        auth_data = signin_response.json()
        token = auth_data.get('access_token')
        print("Signin successful!")
    else:
        print(f"Signin failed: {signin_response.text}")
        exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Test creating a task with new fields
print("\nTesting task creation with advanced fields...")
task_data = {
    "title": "Test Advanced Task",
    "description": "This is a test task with priority and due date",
    "priority": "high",
    "dueDate": "2025-12-31T10:00:00Z",
    "category": "work"
}

task_response = requests.post(f"{BASE_URL}/api/tasks/", json=task_data, headers=headers)
print(f"Task creation status: {task_response.status_code}")
if task_response.status_code == 200:
    created_task = task_response.json()
    print(f"Task created successfully: {created_task['title']}")
    print(f"Task priority: {created_task.get('priority', 'Not found')}")
    print(f"Task due date: {created_task.get('due_date', 'Not found')}")
    print(f"Task category: {created_task.get('category', 'Not found')}")
else:
    print(f"Task creation failed: {task_response.text}")

# Test getting tasks
print("\nTesting task retrieval...")
get_tasks_response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)
print(f"Get tasks status: {get_tasks_response.status_code}")
if get_tasks_response.status_code == 200:
    tasks = get_tasks_response.json()
    print(f"Retrieved {len(tasks)} tasks")
    if tasks:
        task = tasks[0]
        print(f"Sample task: {task['title']}")
        print(f"Priority: {task.get('priority', 'Not found')}")
        print(f"Due date: {task.get('due_date', 'Not found')}")
        print(f"Category: {task.get('category', 'Not found')}")
else:
    print(f"Get tasks failed: {get_tasks_response.text}")