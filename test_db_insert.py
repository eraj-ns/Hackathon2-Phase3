import os
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import Session, select
from src.database import engine
from src.models.user import User
import uuid
from datetime import datetime, timezone
from passlib.context import CryptContext

# Test database connection and insertion
try:
    print("Testing database connection...")

    with Session(engine) as session:
        print("Session created successfully")

        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
        if existing_user:
            print("User already exists")
        else:
            print("No existing user found, proceeding with creation")

            # Hash the password - use same config as auth router
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b", bcrypt__rounds=12)
            hashed_password = pwd_context.hash("password123")
            
            # Create new user
            user_id = f"user_{str(uuid.uuid4()).replace('-', '')}"
            
            user = User(
                id=user_id,
                email="test@example.com",
                hashedPassword=hashed_password,
                name="Test User"
                # createdAt and updatedAt will be set by the database
            )
            
            print(f"Creating user with ID: {user_id}")
            session.add(user)
            session.commit()
            print("User committed successfully")
            
            session.refresh(user)
            print(f"User created with ID: {user.id}, Email: {user.email}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()