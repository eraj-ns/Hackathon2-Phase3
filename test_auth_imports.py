#!/usr/bin/env python3
"""
Test script to check if there are any import errors in the auth router
"""

try:
    print("Testing imports...")
    from src.api.auth_router import router
    print("✓ Auth router imported successfully")
    
    from src.models.user import User
    print("✓ User model imported successfully")
    
    from src.database import get_session
    print("✓ Database session imported successfully")
    
    from src.dependencies import SECRET_KEY, ALGORITHM
    print(f"✓ Dependencies imported successfully. Secret key length: {len(SECRET_KEY) if SECRET_KEY else 0}")
    
    print("\nAll imports successful! The auth router should work.")
    
except Exception as e:
    print(f"✗ Error importing: {e}")
    import traceback
    traceback.print_exc()