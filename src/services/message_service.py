"""Message service for the AI Chat Agent & Conversation System."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from ..models.message import Message, MessageCreate, MessageRead


class MessageService:
    """Service class for handling message-related operations."""

    def create_message(
        self,
        session: Session,
        conversation_id: UUID,
        user_id: UUID,
        role: str,
        content: str,
        message_metadata: Optional[dict] = None
    ) -> Message:
        """Create a new message in a conversation."""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            message_metadata=message_metadata
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def get_message_by_id(
        self,
        session: Session,
        message_id: UUID
    ) -> Optional[Message]:
        """Get a message by its ID."""
        statement = select(Message).where(Message.id == message_id)
        return session.exec(statement).first()

    def get_messages_by_conversation(
        self,
        session: Session,
        conversation_id: UUID,
        offset: int = 0,
        limit: int = 20,
        role_filter: Optional[str] = None
    ) -> List[Message]:
        """Get messages from a specific conversation with pagination."""
        statement = select(Message).where(Message.conversation_id == conversation_id)

        if role_filter:
            statement = statement.where(Message.role == role_filter)

        statement = (
            statement
            .order_by(Message.created_at.asc())
            .offset(offset)
            .limit(limit)
        )

        return session.exec(statement).all()

    def get_recent_messages(
        self,
        session: Session,
        conversation_id: UUID,
        limit: int = 10
    ) -> List[Message]:
        """Get the most recent messages from a conversation."""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        return session.exec(statement).all()

    def count_messages_in_conversation(
        self,
        session: Session,
        conversation_id: UUID
    ) -> int:
        """Count the total number of messages in a conversation."""
        from sqlmodel import func
        statement = select(func.count(Message.id)).where(Message.conversation_id == conversation_id)
        return session.exec(statement).one()

    def update_message_metadata(
        self,
        session: Session,
        message_id: UUID,
        metadata: dict
    ) -> Optional[Message]:
        """Update the metadata of a message."""
        message = self.get_message_by_id(session, message_id)
        if message:
            if message.message_metadata:
                message.message_metadata.update(metadata)
            else:
                message.message_metadata = metadata
            message.updated_at = datetime.utcnow()
            session.add(message)
            session.commit()
            session.refresh(message)
        return message

    def delete_message(self, session: Session, message_id: UUID) -> bool:
        """Delete a message (hard delete)."""
        message = self.get_message_by_id(session, message_id)
        if message:
            session.delete(message)
            session.commit()
            return True
        return False