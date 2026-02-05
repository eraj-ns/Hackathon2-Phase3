from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"
    """
    User model matching Better Auth 'users' table schema for SQLModel backend queries.
    """
    id: str = Field(primary_key=True)

    name: Optional[str] = Field(default=None, max_length=255)

    email: str = Field(index=True, unique=True, max_length=320)

    image: Optional[str] = Field(default=None, max_length=500)

    emailVerified: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True))
    )

    hashedPassword: Optional[str] = Field(default=None)

    createdAt: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now()
        )
    )

    updatedAt: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    # Relationships - for SQLModel compatibility
    conversations: List["Conversation"] = Relationship(back_populates="user")
    messages: List["Message"] = Relationship(back_populates="user")