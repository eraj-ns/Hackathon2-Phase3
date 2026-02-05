#!/usr/bin/env python3
"""
Explicit database table creation script for Todo App Backend.
This script creates the Task table in Neon PostgreSQL and verifies creation.
"""

import os
import sys
import time

# Manually load .env file first (before any imports)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                value = value.strip('"\'')
                os.environ[key] = value

# Debug: Print if DATABASE_URL is loaded
print(f"DEBUG: DATABASE_URL loaded: {'Yes' if os.getenv('DATABASE_URL') else 'No'}")
if os.getenv('DATABASE_URL'):
    print(f"DEBUG: URL preview: {os.getenv('DATABASE_URL')[:50]}...")
else:
    print("DEBUG: DATABASE_URL is NOT set")

# Add the current directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import create_db_and_tables, engine


def create_tables():
    """Create database tables."""
    print("🔌 Connecting to Neon PostgreSQL...")
    print(f"   Database URL: {os.getenv('DATABASE_URL', 'Not set')[:50]}...")

    try:
        # Test connection
        print("\n📊 Testing database connection...")
        connection = engine.connect()
        connection.close()
        print("   ✅ Database connection successful")

        # Create tables
        print("\n🏗️  Creating tables...")

        # Import the models to ensure they're registered with SQLModel
        from src.models.task import Task
        from src.models.user import User
        from src.models.conversation import Conversation
        from src.models.message import Message

        create_db_and_tables()
        print("   ✅ Tables created successfully")

        return True

    except Exception as e:
        print(f"\n   ❌ Error: {str(e)}")
        return False


def verify_tables():
    """Verify tables were created."""
    print("\n🔍 Verifying tables exist...")

    try:
        from sqlmodel import SQLModel
        from src.models.task import Task

        # Get table info
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()

        print(f"   Tables in database: {tables}")

        if 'task' in tables:
            print("\n   ✅ Task table exists!")

            # Get column info
            columns = inspector.get_columns('task')
            print(f"\n   📋 Task table columns:")
            for col in columns:
                print(f"      - {col['name']}: {col['type']}")

            return True
        else:
            print("\n   ❌ Task table not found")
            return False

    except Exception as e:
        print(f"\n   ❌ Error verifying tables: {str(e)}")
        return False


def main():
    """Main execution."""
    print("=" * 60)
    print("Todo App - Database Table Creation")
    print("=" * 60)

    # Check environment
    if not os.getenv('DATABASE_URL'):
        print("❌ DATABASE_URL environment variable not set")
        print("   Please check your .env file at:", env_path)
        return False

    # Create tables
    if not create_tables():
        return False

    # Give it a moment
    time.sleep(1)

    # Verify tables
    if not verify_tables():
        return False

    print("\n" + "=" * 60)
    print("✅ All tables created and verified successfully!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Run the server: python3 src/main.py")
    print("2. Test the API at: http://localhost:8000/docs")
    print("3. Or use this script to verify tables anytime")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
