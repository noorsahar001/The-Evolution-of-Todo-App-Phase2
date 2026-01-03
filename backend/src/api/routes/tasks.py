"""Task routes.

Per spec.md REST API Endpoints:
- GET /api/tasks - List user's tasks (200 OK)
- POST /api/tasks - Create new task (201 Created)
- GET /api/tasks/{id} - Get single task (200 OK)
- PUT /api/tasks/{id} - Update task (200 OK)
- DELETE /api/tasks/{id} - Delete task (204 No Content)
- PATCH /api/tasks/{id}/toggle - Toggle completion (200 OK)

Per FR-017: All endpoints require valid JWT authentication.
Per FR-011: Users can only access their own tasks.
Per Constitution VII: Extract user_id from JWT only.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..deps import get_db, get_current_user
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..schemas.error import ErrorCode
from ...models.user import User
from ...services.task import (
    list_tasks,
    get_task,
    create_task,
    update_task,
    delete_task,
    toggle_task,
)

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get(
    "",
    response_model=list[TaskResponse],
    responses={
        401: {"description": "Not authenticated"},
    },
)
def get_tasks(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TaskResponse]:
    """List all tasks for the authenticated user.

    Per FR-011, FR-017, US3: Return only tasks owned by the current user.
    Per Constitution VII: user_id extracted from JWT via get_current_user.
    """
    tasks = list_tasks(session=session, user_id=current_user.id)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Validation error"},
        401: {"description": "Not authenticated"},
    },
)
def create_new_task(
    task_data: TaskCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """Create a new task for the authenticated user.

    Per FR-009, FR-010, US4: Accept title (required) and description (optional).
    Per FR-015: Auto-assign user_id from JWT.
    Per FR-016: Set is_completed=False by default.
    Per FR-017: Requires valid JWT.
    """
    task = create_task(
        session=session,
        user_id=current_user.id,  # Per FR-015, Constitution VII
        title=task_data.title,
        description=task_data.description,
    )
    return TaskResponse.model_validate(task)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized to access this task"},
        404: {"description": "Task not found"},
    },
)
def get_single_task(
    task_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """Get a specific task by ID.

    Per FR-011, FR-017: Only return if owned by current user.
    Per FR-019: Return 403 FORBIDDEN if accessing another user's task.
    Per FR-020: Return 404 NOT_FOUND if task doesn't exist.
    """
    task = get_task(session=session, task_id=task_id, user_id=current_user.id)

    if task is None:
        # Per FR-020: Task not found (or not owned - same response for security)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
            headers={"X-Error-Code": ErrorCode.NOT_FOUND},
        )

    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        400: {"description": "Validation error"},
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized to access this task"},
        404: {"description": "Task not found"},
    },
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """Update an existing task.

    Per FR-012, FR-017, US5: Update title and/or description.
    Per FR-011: Only update if owned by current user.
    Per FR-019: Return 403 FORBIDDEN if accessing another user's task.
    Per FR-020: Return 404 NOT_FOUND if task doesn't exist.
    """
    task = update_task(
        session=session,
        task_id=task_id,
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
    )

    if task is None:
        # Per FR-020: Task not found (or not owned - same response for security)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
            headers={"X-Error-Code": ErrorCode.NOT_FOUND},
        )

    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized to access this task"},
        404: {"description": "Task not found"},
    },
)
def delete_existing_task(
    task_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete an existing task.

    Per FR-013, FR-017, US6: Remove task permanently.
    Per FR-011: Only delete if owned by current user.
    Per FR-019: Return 403 FORBIDDEN if accessing another user's task.
    Per FR-020: Return 404 NOT_FOUND if task doesn't exist.
    """
    deleted = delete_task(session=session, task_id=task_id, user_id=current_user.id)

    if not deleted:
        # Per FR-020: Task not found (or not owned - same response for security)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
            headers={"X-Error-Code": ErrorCode.NOT_FOUND},
        )


@router.patch(
    "/{task_id}/toggle",
    response_model=TaskResponse,
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized to access this task"},
        404: {"description": "Task not found"},
    },
)
def toggle_task_completion(
    task_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """Toggle task completion status.

    Per FR-014, FR-017, US7: Flip is_completed between True and False.
    Per FR-011: Only toggle if owned by current user.
    Per FR-019: Return 403 FORBIDDEN if accessing another user's task.
    Per FR-020: Return 404 NOT_FOUND if task doesn't exist.
    """
    task = toggle_task(session=session, task_id=task_id, user_id=current_user.id)

    if task is None:
        # Per FR-020: Task not found (or not owned - same response for security)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
            headers={"X-Error-Code": ErrorCode.NOT_FOUND},
        )

    return TaskResponse.model_validate(task)
