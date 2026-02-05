"""
Update Task Tool

This module implements the update_task MCP tool for updating existing tasks.
"""

from typing import Dict, Any
from ..error_handler import handle_tool_errors, create_error_response, create_success_response, log_tool_operation
from ..config import config
from ...database import get_session
from ...services.task_service import update_user_task
from uuid import UUID
from ...services.mcp_tool_service import MCPTaskService


@handle_tool_errors("update_task")
def update_task(user_id: str, task_id: str, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
    """
    Updates an existing task for the specified user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
        completed: New completion status for the task (optional)

    Returns:
        Dictionary with updated task information
    """
    # Log the operation
    log_tool_operation("update_task", user_id=user_id, task_id=task_id)

    # Validate inputs
    if not user_id or not task_id:
        return create_error_response(
            "validation_error",
            "user_id and task_id are required fields"
        )

    # Validate UUID formats
    user_uuid_validation = MCPTaskService.validate_uuid_format(user_id, "user_id")
    if not user_uuid_validation["valid"]:
        return create_error_response(
            user_uuid_validation["error"]["type"],
            user_uuid_validation["error"]["message"]
        )

    task_uuid_validation = MCPTaskService.validate_uuid_format(task_id, "task_id")
    if not task_uuid_validation["valid"]:
        return create_error_response(
            task_uuid_validation["error"]["type"],
            task_uuid_validation["error"]["message"]
        )

    # Validate that user exists
    if not MCPTaskService.validate_user_exists(user_id):
        return create_error_response(
            "user_not_found",
            "User not found"
        )

    # Validate input parameters
    params = {"user_id": user_id, "task_id": task_id}
    required_params = ["user_id", "task_id"]
    validation_result = MCPTaskService.validate_input_parameters(params, required_params)
    if not validation_result["valid"]:
        return create_error_response(
            validation_result["error"]["type"],
            validation_result["error"]["message"]
        )

    # Validate title length if provided
    if title and len(title) > 255:
        return create_error_response(
            "validation_error",
            "Title must be less than 255 characters"
        )

    # Validate description length if provided
    if description and len(description) > 1000:
        return create_error_response(
            "validation_error",
            "Description must be less than 1000 characters"
        )

    # Validate that the user can access the task
    access_validation = MCPTaskService.validate_user_can_access_task(user_id, task_id)
    if not access_validation["valid"]:
        return create_error_response(
            access_validation["error"]["type"],
            access_validation["error"]["message"]
        )

    # Prepare update fields
    update_fields = {}
    if title is not None:
        update_fields['title'] = title
    if description is not None:
        update_fields['description'] = description
    if completed is not None:
        update_fields['completed'] = completed

    # Update task using the existing service
    try:
        with next(get_session()) as session:
            task = update_user_task(session, user_id, task_id, **update_fields)

            if not task:
                return create_error_response(
                    "not_found",
                    "Task not found or does not belong to the user"
                )

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
        }, "Task updated successfully")
    except Exception as e:
        return create_error_response(
            "server_error",
            f"Failed to update task: {str(e)}"
        )