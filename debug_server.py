import os
from dotenv import load_dotenv
load_dotenv()

import uvicorn
from src.main import app

if __name__ == "__main__":
    # Run with debug mode to see detailed errors
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug"
    )