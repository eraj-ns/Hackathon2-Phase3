"""Intent model for the AI Chat Agent & Conversation System."""

from enum import Enum
from typing import List
from pydantic import BaseModel


class IntentType(str, Enum):
    """Enumeration of possible intent types for task operations."""
    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    VIEW_TASKS = "view_tasks"
    SEARCH_TASKS = "search_tasks"
    MARK_COMPLETE = "mark_complete"
    MARK_INCOMPLETE = "mark_incomplete"
    UNKNOWN = "unknown"


class Intent(BaseModel):
    """Classification of user input intent for task operations."""

    type: IntentType
    confidence: float  # 0.0 to 1.0
    parameters: dict   # Specific parameters for the intent
    extracted_entities: List[str]  # Named entities extracted from the message


class IntentRecognitionResult(BaseModel):
    """Result of intent recognition process."""

    intent: Intent
    raw_text: str
    confidence: float