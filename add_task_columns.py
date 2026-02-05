"""
Database Migration Script
Adds priority, due_date, and category columns to the tasks table
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent / "backend"
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
def load_env():
    env_file = project_root / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip("'\"")

# Load environment
load_env()

from sqlmodel import SQLModel, create_engine, Session
from src.models.task import Task

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine
engine = create_engine(DATABASE_URL)

def migrate():
    """Run the migration to add new columns to tasks table."""
    print("Starting database migration...")
    
    # Create tables (this will add new columns if they don't exist)
    # Note: SQLModel doesn't automatically handle schema migrations for existing tables
    # We need to manually alter the table
    
    from sqlalchemy import text
    
    with engine.connect() as conn:
        # Add priority column with default value
        try:
            conn.execute(text("ALTER TABLE task ADD COLUMN priority VARCHAR(20) DEFAULT 'medium';"))
            print("Added priority column")
        except Exception as e:
            print(f"Priority column may already exist: {e}")
        
        # Add due_date column
        try:
            conn.execute(text("ALTER TABLE task ADD COLUMN due_date TIMESTAMP WITH TIME ZONE;"))
            print("Added due_date column")
        except Exception as e:
            print(f"Due date column may already exist: {e}")
        
        # Add category column
        try:
            conn.execute(text("ALTER TABLE task ADD COLUMN category VARCHAR(255);"))
            print("Added category column")
        except Exception as e:
            print(f"Category column may already exist: {e}")
        
        # Commit the transaction
        conn.commit()
    
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()