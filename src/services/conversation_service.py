"""Conversation service for the AI Chat Agent & Conversation System."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from ..models.conversation import Conversation, ConversationCreate, ConversationRead
from ..models.message import Message


class ConversationService:
    """Service class for handling conversation-related operations."""

    def create_conversation(
        self,
        session: Session,
        user_id: UUID,
        title: str,
        is_active: bool = True
    ) -> Conversation:
        """Create a new conversation for a user."""
        conversation = Conversation(
            user_id=user_id,
            title=title,
            is_active=is_active
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_conversation_by_id(
        self,
        session: Session,
        conversation_id: UUID
    ) -> Optional[Conversation]:
        """Get a conversation by its ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    def get_conversations_by_user(
        self,
        session: Session,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        sort_by: str = "updated_at",
        order: str = "desc"
    ) -> List[Conversation]:
        """Get all conversations for a specific user with pagination."""
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .offset(offset)
            .limit(limit)
        )

        # Add sorting
        if sort_by == "updated_at":
            if order == "desc":
                statement = statement.order_by(Conversation.updated_at.desc())
            else:
                statement = statement.order_by(Conversation.updated_at.asc())
        elif sort_by == "created_at":
            if order == "desc":
                statement = statement.order_by(Conversation.created_at.desc())
            else:
                statement = statement.order_by(Conversation.created_at.asc())
        elif sort_by == "title":
            if order == "desc":
                statement = statement.order_by(Conversation.title.desc())
            else:
                statement = statement.order_by(Conversation.title.asc())

        return session.exec(statement).all()

    def update_conversation_title(
        self,
        session: Session,
        conversation_id: UUID,
        title: str
    ) -> Optional[Conversation]:
        """Update the title of a conversation."""
        conversation = self.get_conversation_by_id(session, conversation_id)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    def archive_conversation(
        self,
        session: Session,
        conversation_id: UUID
    ) -> Optional[Conversation]:
        """Archive a conversation by setting is_active to False."""
        conversation = self.get_conversation_by_id(session, conversation_id)
        if conversation:
            conversation.is_active = False
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    def delete_conversation(
        self,
        session: Session,
        conversation_id: UUID
    ) -> bool:
        """Soft delete a conversation by marking it as inactive."""
        conversation = self.get_conversation_by_id(session, conversation_id)
        if conversation:
            conversation.is_active = False
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            return True
        return False

    def get_message_count(
        self,
        session: Session,
        conversation_id: UUID
    ) -> int:
        """Get the count of messages in a conversation."""
        from ..services.message_service import MessageService
        message_service = MessageService()
        return message_service.count_messages_in_conversation(session, conversation_id)