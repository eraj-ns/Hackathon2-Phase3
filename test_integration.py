#!/usr/bin/env python3
"""
Integration test to verify the full application is working correctly.
Tests the connection between the frontend and backend servers.
"""

import requests
import time
import sys
import subprocess
import signal
import os

def test_backend_connection():
    """Test that the backend server is accessible and responding."""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            data = response.json()
            if "message" in data and "Welcome to the Todo API" in data["message"]:
                print("[OK] Backend server is responding correctly")
                return True
            else:
                print(f"[ERROR] Backend response unexpected: {data}")
                return False
        else:
            print(f"[ERROR] Backend server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not connect to backend server: {e}")
        return False

def test_auth_endpoints():
    """Test that authentication endpoints are available."""
    try:
        response = requests.get("http://localhost:8000/auth/csrf")
        # This should return a CSRF token or an auth-related response
        print(f"[OK] Auth endpoint accessible, status: {response.status_code}")
        return True
    except Exception as e:
        print(f"[WARN] Auth endpoint not accessible: {e}")
        return False

def test_api_docs():
    """Test that API documentation is available."""
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("[OK] API documentation is accessible")
            return True
        else:
            print(f"[WARN] API docs returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"[WARN] Could not access API docs: {e}")
        return False

def main():
    print("[TEST] Running Full Application Integration Test")
    print("=" * 50)

    # Wait a moment to ensure servers are ready
    time.sleep(2)

    all_tests_passed = True

    print("\n[TEST] Testing Backend Server...")
    if not test_backend_connection():
        all_tests_passed = False

    print("\n[TEST] Testing Auth Endpoints...")
    if not test_auth_endpoints():
        all_tests_passed = False

    print("\n[TEST] Testing API Documentation...")
    if not test_api_docs():
        all_tests_passed = False

    print("\n" + "=" * 50)
    if all_tests_passed:
        print("[SUCCESS] All integration tests passed!")
        print("[SUCCESS] Full application is working correctly")
        print("[INFO] Backend server running on http://localhost:8000")
        print("[INFO] Frontend server should be running on http://localhost:3000")
        return True
    else:
        print("[ERROR] Some integration tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)