#!/usr/bin/env python
"""
Debug script to test imports in the backend application
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

print("Testing imports...")

try:
    from src.database import create_db_and_tables, get_session
    print("[OK] Successfully imported database module")
except Exception as e:
    print(f"[FAIL] Failed to import database module: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.models.user import User
    print("[OK] Successfully imported User model")
except Exception as e:
    print(f"[FAIL] Failed to import User model: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.dependencies import get_current_user
    print("[OK] Successfully imported dependencies")
except Exception as e:
    print(f"[FAIL] Failed to import dependencies: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.api.tasks_router import router as tasks_router
    print("[OK] Successfully imported tasks router")
except Exception as e:
    print(f"[FAIL] Failed to import tasks router: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.api.auth_router import router as auth_router
    print("[OK] Successfully imported auth router")
except Exception as e:
    print(f"[FAIL] Failed to import auth router: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.main import app
    print("[OK] Successfully imported main app")
except Exception as e:
    print(f"[FAIL] Failed to import main app: {e}")
    import traceback
    traceback.print_exc()

print("\nAll imports tested!")