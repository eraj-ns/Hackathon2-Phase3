import subprocess
import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    from src.main import app

    print("Starting backend server...")
    print(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')}")
    print("Listening on http://localhost:8000")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False  # Set to True if you want hot reloading during development
    )