"""
Add Task Tool

This module implements the add_task MCP tool for creating new tasks.
"""

from typing import Dict, Any
from ..error_handler import handle_tool_errors, create_error_response, create_success_response, log_tool_operation
from ..config import config
from ...database import get_session
from ...services.task_service import create_task
from uuid import UUID
from ...services.mcp_tool_service import MCPTaskService


@handle_tool_errors("add_task")
def add_task(user_id: str, title: str, description: str = "") -> Dict[str, Any]:
    """
    Creates a new task for the specified user.

    Args:
        user_id: The ID of the user for whom to create the task
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dictionary with task creation result
    """
    # Log the operation
    log_tool_operation("add_task", user_id=user_id)

    # Validate inputs
    if not user_id or not title:
        return create_error_response(
            "validation_error",
            "user_id and title are required fields"
        )

    # Validate UUID format
    uuid_validation = MCPTaskService.validate_uuid_format(user_id, "user_id")
    if not uuid_validation["valid"]:
        return create_error_response(
            uuid_validation["error"]["type"],
            uuid_validation["error"]["message"]
        )

    # Validate that user exists
    if not MCPTaskService.validate_user_exists(user_id):
        return create_error_response(
            "user_not_found",
            "User not found"
        )

    # Validate input parameters
    params = {"user_id": user_id, "title": title}
    required_params = ["user_id", "title"]
    validation_result = MCPTaskService.validate_input_parameters(params, required_params)
    if not validation_result["valid"]:
        return create_error_response(
            validation_result["error"]["type"],
            validation_result["error"]["message"]
        )

    # Validate title length
    if len(title) > 255:
        return create_error_response(
            "validation_error",
            "Title must be less than 255 characters"
        )

    # Validate description length
    if description and len(description) > 1000:
        return create_error_response(
            "validation_error",
            "Description must be less than 1000 characters"
        )

    # Create task using the existing service
    try:
        with next(get_session()) as session:
            task = create_task(
                session=session,
                title=title,
                user_id=user_id,
                description=description
            )

        # Return success response
        return create_success_response({
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description or "",
                "completed": getattr(task, 'completed', False),
                "user_id": str(task.user_id),
                "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None,
                "updated_at": task.updated_at.isoformat() if hasattr(task, 'updated_at') else None
            }
        }, "Task created successfully")
    except Exception as e:
        return create_error_response(
            "server_error",
            f"Failed to create task: {str(e)}"
        )