"""
Environment Configuration Management for MCP Server

This module handles configuration management for the MCP server.
"""

import os
from typing import Optional

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    import pathlib
    # Load from the backend directory
    env_path = pathlib.Path(__file__).parent.parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Try loading from the backend directory
        env_path = pathlib.Path(__file__).parent.parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
except ImportError:
    # If dotenv is not available, continue without loading .env
    pass


class MCPConfig:
    """Configuration class for MCP server settings."""

    # Server configuration
    @staticmethod
    def get_host() -> str:
        """Get the host for the MCP server."""
        return os.getenv("MCP_SERVER_HOST", "localhost")

    @staticmethod
    def get_port() -> int:
        """Get the port for the MCP server."""
        port_str = os.getenv("MCP_SERVER_PORT", "3000")
        try:
            return int(port_str)
        except ValueError:
            return 3000  # default port

    @staticmethod
    def get_debug_mode() -> bool:
        """Get the debug mode setting."""
        debug_str = os.getenv("MCP_DEBUG", "false").lower()
        return debug_str in ['true', '1', 'yes', 'on']

    @staticmethod
    def get_log_level() -> str:
        """Get the log level setting."""
        return os.getenv("MCP_LOG_LEVEL", "INFO")

    @staticmethod
    def get_database_url() -> Optional[str]:
        """Get the database URL."""
        return os.getenv("DATABASE_URL")

    @staticmethod
    def get_allowed_origins() -> str:
        """Get allowed origins for CORS (if applicable)."""
        return os.getenv("MCP_ALLOWED_ORIGINS", "*")

    @staticmethod
    def get_max_concurrent_requests() -> int:
        """Get maximum concurrent requests allowed."""
        max_requests_str = os.getenv("MCP_MAX_CONCURRENT_REQUESTS", "100")
        try:
            return int(max_requests_str)
        except ValueError:
            return 100  # default value

    @staticmethod
    def get_request_timeout() -> int:
        """Get request timeout in seconds."""
        timeout_str = os.getenv("MCP_REQUEST_TIMEOUT", "30")
        try:
            return int(timeout_str)
        except ValueError:
            return 30  # default timeout in seconds

    @staticmethod
    def validate_config() -> tuple[bool, str]:
        """
        Validate the configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if database URL is set
        db_url = MCPConfig.get_database_url()
        if not db_url:
            return False, "DATABASE_URL environment variable is not set"

        # Validate port number
        try:
            port = MCPConfig.get_port()
            if port < 1 or port > 65535:
                return False, f"Port number {port} is outside valid range (1-65535)"
        except ValueError:
            return False, "Invalid port number in MCP_SERVER_PORT environment variable"

        return True, ""


# Initialize configuration
config = MCPConfig()

# Optionally validate configuration (can be disabled for testing)
def initialize_config(perform_validation: bool = True):
    if perform_validation:
        is_valid, error_msg = config.validate_config()
        if not is_valid:
            raise ValueError(f"MCP Server configuration error: {error_msg}")
    return config

# By default, don't raise an exception on import to allow testing
# The validation will be performed when the server starts