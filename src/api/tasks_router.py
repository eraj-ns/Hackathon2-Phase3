from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from ..database import get_session
from ..models.task import Task
from ..services import task_service
from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    dueDate: Optional[str] = None
    category: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    dueDate: Optional[str] = None
    category: Optional[str] = None


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create a new task."""
    if not task.title or task.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title is required and cannot be empty"
        )

    new_task = task_service.create_task(
        session=db,
        title=task.title,
        user_id=current_user.id,
        description=task.description,
        priority=task.priority,
        due_date=task.dueDate,
        category=task.category
    )
    return new_task


@router.get("/", response_model=List[Task])
def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get user's tasks."""
    return task_service.list_user_tasks(db, current_user.id)


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get user's task by ID."""
    task = task_service.get_user_task(db, current_user.id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this task"
        )
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update user's task."""
    # Build update fields
    update_fields = {}
    if task_update.title is not None:
        update_fields['title'] = task_update.title
    if task_update.description is not None:
        update_fields['description'] = task_update.description
    if task_update.completed is not None:
        update_fields['completed'] = task_update.completed
    if task_update.priority is not None:
        update_fields['priority'] = task_update.priority
    if task_update.dueDate is not None:
        update_fields['due_date'] = task_update.dueDate
    if task_update.category is not None:
        update_fields['category'] = task_update.category

    if not update_fields:
        task = task_service.get_user_task(db, current_user.id, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this task"
            )
        return task

    updated_task = task_service.update_user_task(db, current_user.id, task_id, **update_fields)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this task"
        )
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete user's task."""
    success = task_service.delete_user_task(db, current_user.id, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this task"
        )
    return None


@router.patch("/{task_id}/complete", response_model=Task)
def toggle_task_complete(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Toggle user's task completion status."""
    task = task_service.get_user_task(db, current_user.id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this task"
        )

    updated_task = task_service.update_user_task(db, current_user.id, task_id, completed=not task.completed)
    return updated_task
