"""Conversation model for the AI Chat Agent & Conversation System."""

from datetime import datetime
from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .message import Message
    from .user import User


class ConversationBase(SQLModel):
    """Base class for Conversation model with common fields."""
    title: str = Field(max_length=255, nullable=False)
    is_active: bool = Field(default=True, nullable=False)


class Conversation(ConversationBase, table=True):
    """Represents a logical conversation thread between a user and the AI agent."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False)  # Links to existing User model (using str ID)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass


class ConversationRead(ConversationBase):
    """Schema for reading conversation data."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
    message_count: int = 0