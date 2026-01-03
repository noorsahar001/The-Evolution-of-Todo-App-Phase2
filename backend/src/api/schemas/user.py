"""User API schemas.

Per FR-001: System MUST allow users to register with email and password.
Per FR-002: System MUST enforce password minimum length of 8 characters.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration.

    Per FR-001, FR-002: Email and password with min 8 characters.
    """

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)",
    )


class UserLogin(BaseModel):
    """Schema for user login.

    Per FR-004: System MUST allow registered users to log in.
    """

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    """Schema for user response (no password).

    Per data-model.md: User response excludes hashed_password.
    """

    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
