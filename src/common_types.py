"""Common type definitions used across the AI Chat Agent & Conversation System."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from uuid import UUID, uuid4
from pydantic import BaseModel

__all__ = [
    "datetime",
    "Enum",
    "List",
    "Optional",
    "Dict",
    "Any",
    "UUID",
    "uuid4",
    "BaseModel",
    "Union",
]


# MCP Tool Response Structures
class SuccessResponse(BaseModel):
    """Structure for successful MCP tool responses."""
    success: bool = True
    data: Dict[str, Any]
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Structure for error MCP tool responses."""
    success: bool = False
    error: Dict[str, Any]


class TaskResponse(BaseModel):
    """Structure for task-related responses."""
    id: str
    title: str
    description: Optional[str] = ""
    completed: bool
    user_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class TaskListResponse(BaseModel):
    """Structure for task list responses."""
    tasks: List[TaskResponse]
    total: int


class ToolResponse(BaseModel):
    """Generic tool response structure."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    message: Optional[str] = None