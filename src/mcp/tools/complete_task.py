"""
Complete Task Tool

This module implements the complete_task MCP tool for marking tasks as completed.
"""

from typing import Dict, Any
from ..error_handler import handle_tool_errors, create_error_response, create_success_response, log_tool_operation
from ..config import config
from .update_task import update_task
from ...services.mcp_tool_service import MCPTaskService


@handle_tool_errors("complete_task")
def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Marks a task as completed for the specified user.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to mark as completed

    Returns:
        Dictionary with updated task information
    """
    # Log the operation
    log_tool_operation("complete_task", user_id=user_id, task_id=task_id)

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

    # Call the update_task function with completed=True
    return update_task(user_id, task_id, completed=True)