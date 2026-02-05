from typing import Optional, List
from sqlmodel import Session, select
from ..models.task import Task
from datetime import datetime


def create_task(session: Session, title: str, user_id: str, description: Optional[str] = None, priority: str = "medium", due_date: Optional[str] = None, category: Optional[str] = None) -> Task:
    """Create a new task."""
    # Convert due_date string to datetime if provided
    due_datetime = None
    if due_date:
        try:
            # Handle ISO format dates with timezone
            due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except ValueError:
            try:
                # Handle dates without timezone
                due_datetime = datetime.fromisoformat(due_date)
            except ValueError:
                # If all parsing fails, use current datetime
                due_datetime = datetime.now()

    task = Task(
        title=title,
        description=description,
        user_id=user_id,
        priority=priority,
        due_date=due_datetime,
        category=category
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_user_task(session: Session, user_id: str, task_id: str) -> Optional[Task]:
    """Get user's task by ID."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    results = session.exec(statement)
    return results.first()


def list_user_tasks(session: Session, user_id: str) -> List[Task]:
    """List user's tasks."""
    statement = select(Task).where(Task.user_id == user_id)
    results = session.exec(statement)
    return results.all()


def update_user_task(session: Session, user_id: str, task_id: str, **fields) -> Optional[Task]:
    """Update user's task."""
    task = get_user_task(session, user_id, task_id)
    if not task:
        return None

    # Map API field names to model field names
    field_mapping = {
        'dueDate': 'due_date',  # API uses camelCase, model uses snake_case
    }

    for key, value in fields.items():
        # Map field name if needed
        model_field = field_mapping.get(key, key)

        if hasattr(task, model_field):
            # Handle due_date conversion if provided as string
            if model_field == 'due_date' and isinstance(value, str):
                try:
                    from datetime import datetime
                    due_datetime = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    setattr(task, model_field, due_datetime)
                except ValueError:
                    import re
                    # Remove timezone info if present and parse
                    date_str = re.sub(r'[+-]\d{2}:?\d{2}$', '', value)  # Remove timezone offset
                    date_str = date_str.rstrip('Z')  # Remove Z suffix
                    due_datetime = datetime.fromisoformat(date_str)
                    setattr(task, model_field, due_datetime)
            else:
                setattr(task, model_field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_user_task(session: Session, user_id: str, task_id: str) -> bool:
    """Delete user's task."""
    task = get_user_task(session, user_id, task_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True
