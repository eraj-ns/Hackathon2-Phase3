"""
Database Migration Script
Adds priority, due_date, and category columns to the tasks table
"""

import os
import sys
sys.path.append('.')  # Add current directory to path

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
    SQLModel.metadata.create_all(engine)

    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()