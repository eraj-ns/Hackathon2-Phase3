import requests
import json
import traceback

# Test the signup endpoint
url = "http://localhost:8000/auth/signup"
headers = {"Content-Type": "application/json"}
data = {
    "email": "debug_test@example.com",
    "password": "testpassword123",
    "name": "Debug Test User"
}

try:
    print("Testing signup endpoint...")
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
    traceback.print_exc()

# Also test the root endpoint
try:
    print("\nTesting root endpoint...")
    response = requests.get("http://localhost:8000/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Root request failed: {e}")
    traceback.print_exc()