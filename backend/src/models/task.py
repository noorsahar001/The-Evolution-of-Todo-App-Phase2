"""Task database model.

Per data-model.md:
- id: Integer (PK, auto-increment)
- title: String(200) [not null]
- description: Text(2000) [nullable]
- is_completed: Boolean [default: false]
- user_id: Integer (FK → User.id)
- created_at: Timestamp [default: now]
- updated_at: Timestamp [on update]

Per FR-010: System MUST associate each task with the creating user (owner).
Per FR-015: System MUST auto-generate unique IDs for tasks.
Per FR-016: System MUST set new tasks as incomplete by default.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task (todo item) model.

    Represents a task owned by a specific user.
    Per Constitution VII: Each task MUST be associated with exactly one user (owner).
    """

    __tablename__ = "task"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False, nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
