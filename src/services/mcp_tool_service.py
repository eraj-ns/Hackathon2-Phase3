"""
MCP Tool Service Module

This module provides common utilities and validation services for MCP tools,
including user validation and database operations.
"""

from typing import Dict, Any, Optional
from uuid import UUID
from sqlmodel import Session, select
from ..models.user import User
from ..models.task import Task
from ..database import get_session


class MCPTaskService:
    """Service class providing common functionality for MCP task tools."""

    @staticmethod
    def validate_user_exists(user_id: str) -> bool:
        """
        Validate that a user exists in the database.

        Args:
            user_id: The ID of the user to validate

        Returns:
            True if user exists, False otherwise
        """
        try:
            UUID(user_id)  # Validate UUID format
        except ValueError:
            return False

        with next(get_session()) as session:
            user = session.get(User, user_id)
            return user is not None

    @staticmethod
    def validate_task_belongs_to_user(session: Session, task_id: str, user_id: str) -> bool:
        """
        Validate that a task belongs to the specified user.

        Args:
            session: Database session
            task_id: The ID of the task to validate
            user_id: The ID of the user who should own the task

        Returns:
            True if task belongs to user, False otherwise
        """
        try:
            UUID(task_id)
            UUID(user_id)
        except ValueError:
            return False

        task = session.get(Task, task_id)
        if not task:
            return False

        return str(task.user_id) == user_id

    @staticmethod
    def validate_user_can_access_task(user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Validate that a user can access a specific task.

        Args:
            user_id: The ID of the user requesting access
            task_id: The ID of the task to access

        Returns:
            Dictionary with validation result and message
        """
        # Check if user exists
        if not MCPTaskService.validate_user_exists(user_id):
            return {
                "valid": False,
                "error": {
                    "type": "user_not_found",
                    "message": "User not found"
                }
            }

        # Check if task exists and belongs to user
        with next(get_session()) as session:
            if not MCPTaskService.validate_task_belongs_to_user(session, task_id, user_id):
                return {
                    "valid": False,
                    "error": {
                        "type": "access_denied",
                        "message": "Task not found or does not belong to the user"
                    }
                }

        return {
            "valid": True,
            "error": None
        }

    @staticmethod
    def validate_input_parameters(params: Dict[str, Any], required_params: list) -> Dict[str, Any]:
        """
        Validate that required parameters are present in input.

        Args:
            params: Input parameters dictionary
            required_params: List of required parameter names

        Returns:
            Dictionary with validation result and message
        """
        missing_params = []
        for param in required_params:
            if param not in params or params[param] is None:
                missing_params.append(param)

        if missing_params:
            return {
                "valid": False,
                "error": {
                    "type": "validation_error",
                    "message": f"Missing required parameters: {', '.join(missing_params)}"
                }
            }

        return {
            "valid": True,
            "error": None
        }

    @staticmethod
    def validate_uuid_format(uuid_str: str, param_name: str = "ID") -> Dict[str, Any]:
        """
        Validate that a string is a valid UUID format.

        Args:
            uuid_str: String to validate as UUID
            param_name: Name of the parameter for error messages

        Returns:
            Dictionary with validation result and message
        """
        try:
            UUID(uuid_str)
            return {
                "valid": True,
                "error": None
            }
        except ValueError:
            return {
                "valid": False,
                "error": {
                    "type": "validation_error",
                    "message": f"Invalid {param_name}: must be a valid UUID"
                }
            }