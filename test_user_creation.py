#!/usr/bin/env python3
"""Test script to debug the authentication issue"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
load_dotenv()

from sqlmodel import create_engine, Session, select
from src.models.user import User
from src.api.auth_router import get_password_hash
import uuid

# Test database connection and user creation directly
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)

def test_user_creation():
    print("Testing user creation directly...")

    # Create a new user
    user_id = f"user_{str(uuid.uuid4()).replace('-', '')}"
    hashed_password = get_password_hash("testpassword123")

    user = User(
        id=user_id,
        email="test_direct@example.com",
        hashedPassword=hashed_password,
        name="Direct Test User"
    )

    print(f"Created user object: {user}")

    try:
        with Session(engine) as session:
            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == user.email)).first()
            if existing_user:
                print("User already exists")
                return

            session.add(user)
            session.commit()
            print("User added successfully!")

            # Refresh to get the created user with any server-side defaults
            session.refresh(user)
            print(f"User refreshed: {user}")

    except Exception as e:
        print(f"Error creating user: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_creation()