"""Task MCP Tools for the AI Chat Agent & Conversation System."""

import asyncio
from typing import List, Dict, Any, Optional
from uuid import UUID

from sqlmodel import Session, select
from sqlmodel.sql.expression import Select

from ..models.task import Task
from ..models.user import User


class TaskMCPTOOLS:
    """MCP tools for task-related operations that the AI agent can use."""

    async def create_task(self, user_id: UUID, title: str, description: str = "", completed: bool = False, session: Session = None) -> Dict[str, Any]:
        """
        Create a new task for the user.

        Args:
            user_id: The ID of the user for whom to create the task
            title: The title of the task
            description: Optional description of the task
            completed: Whether the task is initially completed (default: False)
            session: Database session (if available)

        Returns:
            Dictionary with task information
        """
        if not session:
            raise ValueError("Database session is required for task operations")

        # Clean the title and description by removing command words
        import re

        # Remove common command phrases like "add task", "create task", etc.
        cleaned_title = re.sub(r'^(add|create)\s+(a\s+)?(task\s+to\s+|task\s+|to\s+)', '', title, flags=re.IGNORECASE)

        # Additional cleaning to remove leading command words
        cleaned_title = re.sub(r'^(add|create|new)\s+', '', cleaned_title, flags=re.IGNORECASE)

        # Strip leading/trailing whitespace
        cleaned_title = cleaned_title.strip()

        # If the cleaned title is empty, use the original
        if not cleaned_title:
            cleaned_title = title.strip()

        # Clean the description too
        cleaned_description = re.sub(r'^(add|create)\s+(a\s+)?(task\s+to\s+|task\s+|to\s+)', '', description, flags=re.IGNORECASE)
        cleaned_description = re.sub(r'^(add|create|new)\s+', '', cleaned_description, flags=re.IGNORECASE)
        cleaned_description = cleaned_description.strip()

        if not cleaned_description:
            cleaned_description = description.strip()

        # Create the task object
        task = Task(
            user_id=user_id,
            title=cleaned_title,
            description=cleaned_description,
            completed=completed
        )

        # Add to session and commit
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None
        }

    async def view_tasks(self, user_id: UUID, completed: bool = None, session: Session = None) -> Dict[str, Any]:
        """
        View tasks for the user.

        Args:
            user_id: The ID of the user whose tasks to view
            completed: Filter by completion status (None for all tasks)
            session: Database session (if available)

        Returns:
            Dictionary with list of tasks
        """
        if not session:
            raise ValueError("Database session is required for task operations")

        # Build the query
        query = select(Task).where(Task.user_id == user_id)

        # Apply completed filter if specified
        if completed is not None:
            query = query.where(Task.completed == completed)

        # Execute the query
        tasks = session.exec(query).all()

        # Convert to dictionary format
        task_list = []
        for task in tasks:
            task_dict = {
                "id": str(task.id),
                "user_id": str(task.user_id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None,
                "updated_at": task.updated_at.isoformat() if hasattr(task, 'updated_at') else None
            }
            task_list.append(task_dict)

        return {
            "tasks": task_list,
            "total": len(task_list)
        }

    async def update_task(self, user_id: UUID, task_id: UUID, title: str = None, description: str = None, completed: bool = None, session: Session = None) -> Dict[str, Any]:
        """
        Update a task for the user.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            session: Database session (if available)

        Returns:
            Dictionary with updated task information
        """
        if not session:
            raise ValueError("Database session is required for task operations")

        # Get the task from the database
        task = session.get(Task, task_id)

        # Verify that the task belongs to the user
        if not task or task.user_id != user_id:
            raise ValueError("Task not found or does not belong to the user")

        # Update the task properties if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        # Update the updated_at timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        # Commit the changes
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "updated_at": task.updated_at.isoformat() if hasattr(task, 'updated_at') else None
        }

    async def delete_task(self, user_id: UUID, task_id: UUID, session: Session = None) -> Dict[str, Any]:
        """
        Delete a task for the user.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to delete
            session: Database session (if available)

        Returns:
            Dictionary with deletion confirmation
        """
        if not session:
            raise ValueError("Database session is required for task operations")

        # Get the task from the database
        task = session.get(Task, task_id)

        # Verify that the task belongs to the user
        if not task or task.user_id != user_id:
            raise ValueError("Task not found or does not belong to the user")

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "id": str(task_id),
            "user_id": str(user_id),
            "deleted": True,
            "message": "Task deleted successfully"
        }

    async def mark_task_completed(self, user_id: UUID, task_id: UUID, session: Session = None) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to mark as completed
            session: Database session (if available)

        Returns:
            Dictionary with updated task information
        """
        return await self.update_task(user_id, task_id, completed=True, session=session)

    async def mark_task_incomplete(self, user_id: UUID, task_id: UUID, session: Session = None) -> Dict[str, Any]:
        """
        Mark a task as incomplete.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to mark as incomplete
            session: Database session (if available)

        Returns:
            Dictionary with updated task information
        """
        return await self.update_task(user_id, task_id, completed=False, session=session)