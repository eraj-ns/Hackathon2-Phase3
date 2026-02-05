"""Message model for the AI Chat Agent & Conversation System."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import JSON

if TYPE_CHECKING:
    from .conversation import Conversation
    from .user import User


class MessageBase(SQLModel):
    """Base class for Message model with common fields."""
    conversation_id: UUID = Field(foreign_key="conversation.id", nullable=False)
    user_id: str = Field(foreign_key="users.id", nullable=False)  # Denormalized for query efficiency (using str ID)
    role: str = Field(max_length=20, nullable=False)  # "user", "assistant", "system", "tool"
    content: str = Field(nullable=False)  # The actual message content
    message_metadata: Optional[dict] = Field(default=None, sa_type=JSON)  # Additional metadata (intent, tool_calls, etc.)


class Message(MessageBase, table=True):
    """Represents individual exchanges within a conversation."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    user: "User" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass


class MessageRead(MessageBase):
    """Schema for reading message data."""
    id: UUID
    created_at: datetime