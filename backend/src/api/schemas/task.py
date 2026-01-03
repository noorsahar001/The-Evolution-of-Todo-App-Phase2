"""Task schemas for request/response validation.

Per spec.md REST API Contracts:
- POST /api/tasks accepts title (required), description (optional)
- PUT /api/tasks/{id} accepts title (optional), description (optional)
- All task responses include id, title, description, is_completed, created_at, updated_at
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Per FR-009: Accept title (required) and description (optional).
    Per data-model.md: title max 200 chars, description max 2000 chars.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (required)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional)",
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    Per FR-012: Accept title (optional), description (optional).
    At least one field should be provided for a meaningful update.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Task title (optional)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional)",
    )


class TaskResponse(BaseModel):
    """Schema for task response.

    Per FR-022: Include all task fields in response.
    Per data-model.md: id, title, description, is_completed, created_at, updated_at.
    """

    id: int = Field(..., description="Task unique identifier")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    is_completed: bool = Field(..., description="Task completion status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")

    model_config = {"from_attributes": True}
