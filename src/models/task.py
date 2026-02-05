from typing import Optional
from sqlmodel import SQLModel, Field, Column, String, Boolean, DateTime, func
from datetime import datetime
import uuid


class Task(SQLModel, table=True):
    """Task entity representing a Todo item."""

    id: str = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String, nullable=False))
    description: Optional[str] = None
    completed: bool = Field(default=False, sa_column=Column(Boolean, default=False))
    priority: str = Field(default="medium", sa_column=Column(String, nullable=False))  # low, medium, high
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    category: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
    user_id: str = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))

    def __init__(self, **kwargs):
        if 'id' not in kwargs or kwargs['id'] is None:
            kwargs['id'] = str(uuid.uuid4())
        super().__init__(**kwargs)
