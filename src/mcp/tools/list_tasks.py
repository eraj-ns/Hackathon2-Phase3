"""
List Tasks Tool

This module implements the list_tasks MCP tool for retrieving user tasks.
"""

from typing import Dict, Any
from ..error_handler import handle_tool_errors, create_error_response, create_success_response, log_tool_operation
from ..config import config
from ...database import get_session
from ...services.task_service import list_user_tasks
from uuid import UUID
from ...services.mcp_tool_service import MCPTaskService


@handle_tool_errors("list_tasks")
def list_tasks(user_id: str, completed_only: bool = False, limit: int = 100) -> Dict[str, Any]:
    """
    Retrieves all tasks for the specified user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        completed_only: If true, only return completed tasks; if false, return all tasks (default: false)
        limit: Maximum number of tasks to return (default: 100)

    Returns:
        Dictionary with list of tasks
    """
    # Log the operation
    log_tool_operation("list_tasks", user_id=user_id)

    # Validate inputs
    if not user_id:
        return create_error_response(
            "validation_error",
            "user_id is required"
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

    # Validate limit
    if limit <= 0 or limit > 1000:
        return create_error_response(
            "validation_error",
            "limit must be between 1 and 1000"
        )

    # List tasks using the existing service
    try:
        with next(get_session()) as session:
            tasks = list_user_tasks(session, user_id)

            # Filter by completion status if requested
            if completed_only:
                tasks = [task for task in tasks if getattr(task, 'completed', False)]

            # Limit results if requested
            tasks = tasks[:limit]

        # Format response
        task_list = []
        for task in tasks:
            task_dict = {
                "id": str(task.id),
                "title": task.title,
                "description": task.description or "",
                "completed": getattr(task, 'completed', False),
                "user_id": str(task.user_id),
                "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None,
                "updated_at": task.updated_at.isoformat() if hasattr(task, 'updated_at') else None
            }
            task_list.append(task_dict)

        return create_success_response({
            "tasks": task_list
        }, f"Retrieved {len(task_list)} tasks")
    except Exception as e:
        return create_error_response(
            "server_error",
            f"Failed to list tasks: {str(e)}"
        )