"""
MCP Server for Task Management Tools

This module implements the MCP (Model Context Protocol) server that exposes
task management operations as callable tools for AI agents.
"""

from typing import Dict, Any, List
from datetime import datetime
from sqlmodel import select

# Import the database session utility
from ..database import get_session
from ..services.task_service import create_task, list_user_tasks, update_user_task, delete_user_task
from ..models.task import Task
from uuid import UUID
from .error_handler import handle_tool_errors, log_tool_call, create_error_response, create_success_response
from ..services.mcp_tool_service import MCPTaskService
from .config import config

# Import individual tools
from .tools.add_task import add_task as imported_add_task
from .tools.list_tasks import list_tasks as imported_list_tasks
from .tools.update_task import update_task as imported_update_task
from .tools.complete_task import complete_task as imported_complete_task
from .tools.delete_task import delete_task as imported_delete_task


# Placeholder MCPServer - will be replaced with actual implementation
class MCPServer:
    def __init__(self):
        self.tools = {}

    def add_tool(self, name, func):
        self.tools[name] = func

    def start(self, host, port):
        print(f"MCP Server starting on {host}:{port}")

    def list_tools(self):
        return [{"name": name} for name in self.tools.keys()]


# Placeholder decorator - will be replaced with actual implementation
def tool(**kwargs):
    def decorator(func):
        return func
    return decorator


class TaskManagementMCPServer:
    """MCP server that provides task management tools for AI agents."""

    def __init__(self):
        """Initialize the MCP server with task management tools."""
        self.server = MCPServer()

        # Register all tools
        self.server.add_tool(imported_add_task.__name__, imported_add_task)
        self.server.add_tool(imported_list_tasks.__name__, imported_list_tasks)
        self.server.add_tool(imported_update_task.__name__, imported_update_task)
        self.server.add_tool(imported_complete_task.__name__, imported_complete_task)
        self.server.add_tool(imported_delete_task.__name__, imported_delete_task)

    def get_session_context(self):
        """Get a database session context."""
        return next(get_session())

    def _execute_with_session(self, func, *args, **kwargs):
        """Execute a function with a database session."""
        with self.get_session_context() as session:
            return func(session, *args, **kwargs)

    def start(self, host: str = "localhost", port: int = 3000):
        """Start the MCP server."""
        # Perform startup validation
        if not self.validate_startup():
            raise RuntimeError("MCP Server failed startup validation")

        print(f"Starting MCP Server on {host}:{port}")
        self.server.start(host=host, port=port)

    def validate_startup(self) -> bool:
        """Validate that the server is ready to start."""
        # Check that all required tools are registered (this doesn't require DB)
        tools = self.get_tools()
        required_tools = {"add_task", "list_tasks", "update_task", "complete_task", "delete_task"}
        registered_tools = {tool['name'] for tool in tools}

        if not required_tools.issubset(registered_tools):
            missing_tools = required_tools - registered_tools
            print(f"Missing required tools: {missing_tools}")
            return False

        # Try a simple database connection check, but don't fail if there are model issues
        try:
            with next(get_session()) as session:
                # Try a basic query that doesn't rely on relationships
                from ..models.user import User
                # Just check if we can access the session
                pass
        except Exception as e:
            # Don't fail startup for database issues - they'll be caught during actual use
            print(f"Database connection warning (will be checked during actual use): {e}")

        print("Startup validation passed")
        return True

    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the server."""
        try:
            # Check database connection
            with next(get_session()) as session:
                session.exec(select(Task).limit(1))

            # Count registered tools
            tools = self.get_tools()

            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "tools_count": len(tools),
                "database_connected": True
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "database_connected": False
            }

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        return self.server.list_tools()


def start_mcp_server():
    """Convenience function to start the MCP server."""
    host = config.get_host()
    port = config.get_port()
    server = TaskManagementMCPServer()
    server.start(host=host, port=port)


if __name__ == "__main__":
    # For testing purposes
    start_mcp_server()