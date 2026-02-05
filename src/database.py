from sqlmodel import create_engine, Session
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    import pathlib
    # Load from the backend directory
    env_path = pathlib.Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Try loading from the project root
        env_path = pathlib.Path(__file__).parent.parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
except ImportError:
    # If dotenv is not available, continue without loading .env
    pass

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Don't raise an error during import time to allow for testing
    # The database connection will be validated when actually used
    DATABASE_URL = None

# Create engine with connection pooling for Neon Serverless PostgreSQL
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Enable SQL logging for development
        pool_size=5,  # Connection pool size
        max_overflow=10,  # Additional connections if pool is exhausted
        pool_pre_ping=True,  # Verify connections are alive before using,
    )
else:
    # Create a placeholder engine that will throw an error if actually used
    # This allows imports to work but will fail when DB operations are attempted
    class PlaceholderEngine:
        def __getattr__(self, name):
            raise RuntimeError("DATABASE_URL environment variable is not set")

    engine = PlaceholderEngine()


def create_db_and_tables():
    """Create database tables."""
    from sqlmodel import SQLModel
    # Import models here to ensure they're registered
    from .models.task import Task
    from .models.user import User
    from .models.conversation import Conversation
    from .models.message import Message
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session
