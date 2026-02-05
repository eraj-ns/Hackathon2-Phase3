#!/usr/bin/env python3
"""
Additional test to verify API endpoints are functional.
"""

import requests
import json

def test_api_endpoints():
    print("Testing API endpoints...")

    # Test the base API
    response = requests.get("http://localhost:8000/")
    print(f"Base API: {response.status_code} - {response.json()}")

    # Test the docs endpoint
    response = requests.get("http://localhost:8000/docs")
    print(f"Docs endpoint: {response.status_code}")

    # Test the OpenAPI schema
    response = requests.get("http://localhost:8000/openapi.json")
    if response.status_code == 200:
        schema = response.json()
        print(f"OpenAPI schema: {len(schema.get('paths', {}))} endpoints available")

        # Show some key endpoints
        paths = list(schema.get('paths', {}).keys())[:5]  # First 5 paths
        print(f"Sample endpoints: {paths}")

    # Test auth endpoints
    print("\nTesting auth endpoints:")
    auth_endpoints = [
        "/auth/csrf",
        "/auth/session",
        "/auth/user",
        "/auth/signin",
        "/auth/signup"
    ]

    for endpoint in auth_endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}")
            print(f"  {endpoint}: {response.status_code}")
        except:
            print(f"  {endpoint}: Failed to connect")

    # Test tasks endpoints
    print("\nTesting tasks endpoints:")
    tasks_endpoints = [
        "/api/tasks/",
        "/api/tasks/me",
        "/api/tasks/create",
        "/api/tasks/{id}",
        "/api/tasks/update/{id}",
        "/api/tasks/delete/{id}"
    ]

    for endpoint in tasks_endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint.replace('{id}', '1')}",
                                  allow_redirects=False)  # Prevent redirects to catch auth issues
            print(f"  {endpoint}: {response.status_code}")
        except:
            print(f"  {endpoint}: Failed to connect")

if __name__ == "__main__":
    print("API Endpoint Verification Test")
    print("=" * 40)
    test_api_endpoints()
    print("=" * 40)
    print("API endpoint verification completed.")