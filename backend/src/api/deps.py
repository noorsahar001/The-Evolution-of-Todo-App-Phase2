"""API dependencies.

Per FR-005, FR-006: JWT token management via cookies.
Per FR-017: All task endpoints MUST require valid JWT authentication.
Per Constitution VII: Backend MUST NOT trust any user ID from frontend; extract from JWT only.
"""

from typing import Generator
from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session, select

from ..core.database import get_session
from ..core.security import verify_token
from ..models.user import User
from .schemas.error import ErrorCode


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency.

    Yields:
        Database session
    """
    yield from get_session()


def get_current_user(
    request: Request,
    session: Session = Depends(get_db),
) -> User:
    """Get the current authenticated user from JWT cookie.

    Per FR-006: JWT stored in httpOnly cookie.
    Per FR-017, FR-018: Require valid JWT, return 401 if missing/invalid.
    Per Constitution VII: Extract user ID from JWT only.

    Args:
        request: FastAPI request object
        session: Database session

    Returns:
        Authenticated User object

    Raises:
        HTTPException: 401 if not authenticated
    """
    # Get token from cookie
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in to continue",
            headers={"X-Error-Code": ErrorCode.UNAUTHORIZED},
        )

    # Verify token and extract user ID
    user_id = verify_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in to continue",
            headers={"X-Error-Code": ErrorCode.UNAUTHORIZED},
        )

    # Get user from database
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in to continue",
            headers={"X-Error-Code": ErrorCode.UNAUTHORIZED},
        )

    return user
