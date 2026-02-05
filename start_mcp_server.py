#!/usr/bin/env python
"""
Script to start the MCP server for task management tools
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

if __name__ == "__main__":
    # Import the MCP server from the correct path
    from backend.src.mcp.server import start_mcp_server

    # Start the MCP server
    start_mcp_server()