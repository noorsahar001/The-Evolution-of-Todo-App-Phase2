"""User database model.

Per data-model.md:
- id: Integer (PK, auto-increment)
- email: String(255) [unique, not null]
- hashed_password: String(255) [not null]
- created_at: Timestamp [default: now]
"""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User account model.

    Represents a registered user in the system.
    """

    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        max_length=255,
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
