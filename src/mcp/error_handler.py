"""
Error Handling and Logging Infrastructure for MCP Tools

This module provides centralized error handling and logging for MCP tools.
"""

import logging
from typing import Dict, Any, Optional
from functools import wraps
from ..common_types import ErrorResponse


# Configure logging for MCP tools
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler for MCP-specific logs
file_handler = logging.FileHandler('mcp_tools.log')
file_handler.setLevel(logging.INFO)

# Create a console handler for real-time monitoring
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_tool_call(tool_name: str):
    """
    Decorator to log tool calls and their parameters.

    Args:
        tool_name: Name of the tool being called
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Tool '{tool_name}' called with args: {args}, kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Tool '{tool_name}' completed successfully")
                return result
            except Exception as e:
                logger.error(f"Tool '{tool_name}' failed with error: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator


def log_tool_operation(operation_name: str, user_id: str = None, task_id: str = None):
    """
    Log specific tool operations with user and task context.

    Args:
        operation_name: Name of the operation being performed
        user_id: ID of the user performing the operation
        task_id: ID of the task being operated on
    """
    context_info = f"Operation: {operation_name}"
    if user_id:
        context_info += f", User: {user_id}"
    if task_id:
        context_info += f", Task: {task_id}"

    logger.info(context_info)


def handle_tool_errors(tool_name: str):
    """
    Decorator to handle errors in tool execution and return structured error responses.

    Args:
        tool_name: Name of the tool being called
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except ValueError as e:
                error_response = ErrorResponse(
                    success=False,
                    error={
                        "type": "validation_error",
                        "message": f"Invalid input to {tool_name}: {str(e)}",
                        "tool_name": tool_name
                    }
                ).dict()
                logger.error(f"{tool_name} validation error: {str(e)}")
                return error_response
            except PermissionError as e:
                error_response = ErrorResponse(
                    success=False,
                    error={
                        "type": "permission_error",
                        "message": f"Permission denied in {tool_name}: {str(e)}",
                        "tool_name": tool_name
                    }
                ).dict()
                logger.error(f"{tool_name} permission error: {str(e)}")
                return error_response
            except Exception as e:
                error_response = ErrorResponse(
                    success=False,
                    error={
                        "type": "server_error",
                        "message": f"Server error in {tool_name}: {str(e)}",
                        "tool_name": tool_name
                    }
                ).dict()
                logger.error(f"{tool_name} server error: {str(e)}")
                return error_response
        return wrapper
    return decorator


def create_error_response(error_type: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized error response.

    Args:
        error_type: Type of the error (e.g., validation_error, not_found, server_error)
        message: Human-readable error message
        details: Optional additional error details

    Returns:
        Standardized error response dictionary
    """
    error_obj = {
        "type": error_type,
        "message": message
    }

    if details:
        error_obj["details"] = details

    return {
        "success": False,
        "error": error_obj
    }


def create_success_response(data: Dict[str, Any], message: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a standardized success response.

    Args:
        data: Data to include in the response
        message: Optional success message

    Returns:
        Standardized success response dictionary
    """
    response = {
        "success": True,
        "data": data
    }

    if message:
        response["message"] = message

    return response


# Log startup message
logger.info("MCP Tools error handling and logging infrastructure initialized")