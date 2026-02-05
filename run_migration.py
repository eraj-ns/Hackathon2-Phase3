#!/usr/bin/env python3
"""
Simple Migration Script
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
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

# Now import and run migration
from sqlmodel import SQLModel, create_engine
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