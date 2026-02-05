"""Conversation Manager for the AI Chat Agent & Conversation System."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session

from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService


class ConversationManager:
    """Manages conversation state reconstruction and persistence for stateless AI interactions."""

    def __init__(self):
        self.conversation_service = ConversationService()
        self.message_service = MessageService()

    def create_new_conversation(
        self,
        session: Session,
        user_id: UUID,
        initial_message_content: str
    ) -> Conversation:
        """Create a new conversation with an auto-generated title based on the initial message."""
        # Auto-generate title from the initial message
        title = self._generate_title_from_message(initial_message_content)

        return self.conversation_service.create_conversation(
            session=session,
            user_id=user_id,
            title=title
        )

    def get_or_create_conversation(
        self,
        session: Session,
        user_id: UUID,
        conversation_id: Optional[UUID],
        initial_message_content: Optional[str] = None
    ) -> Conversation:
        """Get an existing conversation or create a new one if conversation_id is not provided."""
        if conversation_id:
            conversation = self.conversation_service.get_conversation_by_id(session, conversation_id)
            if not conversation:
                raise ValueError(f"Conversation with ID {conversation_id} not found")
            if conversation.user_id != user_id:
                raise PermissionError("User does not have access to this conversation")
            return conversation
        elif initial_message_content:
            return self.create_new_conversation(session, user_id, initial_message_content)
        else:
            raise ValueError("Either conversation_id or initial_message_content must be provided")

    def reconstruct_conversation_history(
        self,
        session: Session,
        conversation_id: UUID,
        user_id: UUID
    ) -> List[Message]:
        """Reconstruct the full conversation history from the database for an AI request."""
        # Verify user has access to this conversation
        conversation = self.conversation_service.get_conversation_by_id(session, conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        if conversation.user_id != user_id:
            raise PermissionError("User does not have access to this conversation")

        # Retrieve all messages in the conversation
        messages = self.message_service.get_messages_by_conversation(session, conversation_id)
        return messages

    def save_user_message(
        self,
        session: Session,
        conversation_id: UUID,
        user_id: UUID,
        content: str,
        metadata: Optional[dict] = None
    ) -> Message:
        """Save a user message to the conversation."""
        return self.message_service.create_message(
            session=session,
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=content,
            message_metadata=metadata
        )

    def save_assistant_message(
        self,
        session: Session,
        conversation_id: UUID,
        user_id: UUID,
        content: str,
        metadata: Optional[dict] = None
    ) -> Message:
        """Save an assistant message to the conversation."""
        return self.message_service.create_message(
            session=session,
            conversation_id=conversation_id,
            user_id=user_id,  # Still associated with the user for access control
            role="assistant",
            content=content,
            message_metadata=metadata
        )

    def save_tool_message(
        self,
        session: Session,
        conversation_id: UUID,
        user_id: UUID,
        content: str,
        metadata: Optional[dict] = None
    ) -> Message:
        """Save a tool message to the conversation."""
        return self.message_service.create_message(
            session=session,
            conversation_id=conversation_id,
            user_id=user_id,
            role="tool",
            content=content,
            message_metadata=metadata
        )

    def get_recent_conversations(
        self,
        session: Session,
        user_id: UUID,
        limit: int = 10
    ) -> List[Conversation]:
        """Get the most recent conversations for a user."""
        return self.conversation_service.get_conversations_by_user(
            session=session,
            user_id=user_id,
            limit=limit,
            sort_by="updated_at",
            order="desc"
        )

    def _generate_title_from_message(self, message_content: str) -> str:
        """Generate a conversation title based on the initial message content."""
        # Take the first 50 characters of the message and add "..." if longer
        if len(message_content) > 50:
            title = message_content[:50].strip() + "..."
        else:
            title = message_content.strip()

        # Ensure title is not empty
        if not title.strip():
            title = f"Conversation started at {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        return title

    def update_conversation_title_if_needed(
        self,
        session: Session,
        conversation_id: UUID,
        new_title: str
    ) -> Conversation:
        """Update the conversation title if it's the auto-generated one."""
        conversation = self.conversation_service.get_conversation_by_id(session, conversation_id)
        if conversation:
            # Only update if it's still the auto-generated title
            if conversation.title.startswith("Conversation started at") or len(conversation.title) < 10:
                return self.conversation_service.update_conversation_title(session, conversation_id, new_title)
        return conversation