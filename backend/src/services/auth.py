"""Authentication service.

Per FR-001: System MUST allow users to register with email and password.
Per FR-003: System MUST prevent duplicate email registrations.
Per FR-004: System MUST allow registered users to log in with email and password.
"""

from typing import Optional
from sqlmodel import Session, select

from ..models.user import User
from ..core.security import hash_password, verify_password


def register_user(session: Session, email: str, password: str) -> Optional[User]:
    """Register a new user.

    Per FR-001: Create user with email and password.
    Per FR-003: Check for duplicate email.

    Args:
        session: Database session
        email: User email
        password: Plain text password

    Returns:
        Created User object, or None if email already exists
    """
    # Check for existing user with same email
    statement = select(User).where(User.email == email)
    existing_user = session.exec(statement).first()

    if existing_user:
        return None  # Email already exists

    # Create new user with hashed password
    user = User(
        email=email,
        hashed_password=hash_password(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user.

    Per FR-004: Verify credentials.

    Args:
        session: Database session
        email: User email
        password: Plain text password

    Returns:
        User object if credentials are valid, None otherwise
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
