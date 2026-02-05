"""
Delete Task Tool

This module implements the delete_task MCP tool for deleting tasks.
"""

from typing import Dict, Any
from ..error_handler import handle_tool_errors, create_error_response, create_success_response, log_tool_operation
from ..config import config
from ...database import get_session
from ...services.task_service import delete_user_task
from uuid import UUID
from ...services.mcp_tool_service import MCPTaskService


@handle_tool_errors("delete_task")
def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Deletes a task for the specified user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete

    Returns:
        Dictionary with deletion confirmation
    """
    # Log the operation
    log_tool_operation("delete_task", user_id=user_id, task_id=task_id)

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

    # Validate that the user can access the task
    access_validation = MCPTaskService.validate_user_can_access_task(user_id, task_id)
    if not access_validation["valid"]:
        return create_error_response(
            access_validation["error"]["type"],
            access_validation["error"]["message"]
        )

    # Delete task using the existing service
    try:
        with next(get_session()) as session:
            success = delete_user_task(session, user_id, task_id)

            if not success:
                return create_error_response(
                    "not_found",
                    "Task not found or does not belong to the user"
                )

        return create_success_response({
            "deleted_task_id": task_id
        }, "Task deleted successfully")
    except Exception as e:
        return create_error_response(
            "server_error",
            f"Failed to delete task: {str(e)}"
        )