"""Task service layer.

Per Constitution VII: Backend MUST NOT trust any user ID from frontend; extract from JWT only.
Per FR-011: Users can only access their own tasks.
Per FR-015, FR-016: Auto-assign user_id from JWT and set is_completed=False on create.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Session, select

from ..models.task import Task


def list_tasks(session: Session, user_id: int) -> list[Task]:
    """List all tasks for a specific user.

    Per FR-011, US3: Return only tasks owned by the authenticated user.

    Args:
        session: Database session
        user_id: Authenticated user's ID from JWT

    Returns:
        List of tasks belonging to the user
    """
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    return list(session.exec(statement).all())


def get_task(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """Get a specific task if owned by the user.

    Per FR-011: Only return task if user_id matches.
    Returns None if task doesn't exist or belongs to another user.

    Args:
        session: Database session
        task_id: Task ID to retrieve
        user_id: Authenticated user's ID from JWT

    Returns:
        Task if found and owned by user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return session.exec(statement).first()


def create_task(
    session: Session,
    user_id: int,
    title: str,
    description: Optional[str] = None,
) -> Task:
    """Create a new task for the user.

    Per FR-009, FR-010: Accept title (required) and description (optional).
    Per FR-015: Auto-assign user_id from JWT (not from request body).
    Per FR-016: Set is_completed=False by default.
    Per US4: Create new task flow.

    Args:
        session: Database session
        user_id: Authenticated user's ID from JWT
        title: Task title (required)
        description: Task description (optional)

    Returns:
        Created task
    """
    now = datetime.now(timezone.utc)
    task = Task(
        title=title,
        description=description,
        is_completed=False,  # Per FR-016
        user_id=user_id,  # Per FR-015, Constitution VII
        created_at=now,
        updated_at=now,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(
    session: Session,
    task_id: int,
    user_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[Task]:
    """Update an existing task if owned by the user.

    Per FR-012, US5: Update title and/or description.
    Per FR-011: Only update if user_id matches (ownership validation).

    Args:
        session: Database session
        task_id: Task ID to update
        user_id: Authenticated user's ID from JWT
        title: New title (optional)
        description: New description (optional)

    Returns:
        Updated task if found and owned, None otherwise
    """
    task = get_task(session, task_id, user_id)
    if task is None:
        return None

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    """Delete a task if owned by the user.

    Per FR-013, US6: Remove task permanently.
    Per FR-011: Only delete if user_id matches (ownership validation).

    Args:
        session: Database session
        task_id: Task ID to delete
        user_id: Authenticated user's ID from JWT

    Returns:
        True if deleted, False if not found or not owned
    """
    task = get_task(session, task_id, user_id)
    if task is None:
        return False

    session.delete(task)
    session.commit()
    return True


def toggle_task(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """Toggle task completion status if owned by the user.

    Per FR-014, US7: Flip is_completed between True and False.
    Per FR-011: Only toggle if user_id matches (ownership validation).

    Args:
        session: Database session
        task_id: Task ID to toggle
        user_id: Authenticated user's ID from JWT

    Returns:
        Updated task if found and owned, None otherwise
    """
    task = get_task(session, task_id, user_id)
    if task is None:
        return None

    task.is_completed = not task.is_completed
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
