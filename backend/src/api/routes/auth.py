"""Authentication routes.

Per spec.md REST API Endpoints:
- POST /api/auth/register - Register new user (201 Created)
- POST /api/auth/login - Authenticate user (200 OK + JWT cookie)
- POST /api/auth/logout - End session (200 OK, clears cookie)
"""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session

from ..deps import get_db
from ..schemas.user import UserCreate, UserLogin, UserResponse
from ..schemas.error import ErrorCode
from ...services.auth import register_user, authenticate_user
from ...core.security import create_access_token
from ...core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Validation error"},
        409: {"description": "Email already exists"},
    },
)
def register(
    user_data: UserCreate,
    session: Session = Depends(get_db),
) -> UserResponse:
    """Register a new user.

    Per FR-001: Allow registration with email and password.
    Per FR-002: Enforce password minimum length of 8 characters (validated by schema).
    Per FR-003: Prevent duplicate email registrations.
    Per US1: User registration flow.
    """
    user = register_user(
        session=session,
        email=user_data.email,
        password=user_data.password,
    )

    if user is None:
        # Per FR-003, US1: Email already exists
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
            headers={"X-Error-Code": ErrorCode.CONFLICT},
        )

    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=UserResponse,
    responses={
        401: {"description": "Invalid credentials"},
    },
)
def login(
    response: Response,
    user_data: UserLogin,
    session: Session = Depends(get_db),
) -> UserResponse:
    """Authenticate user and set JWT cookie.

    Per FR-004: Allow login with email and password.
    Per FR-005: Issue JWT token upon successful login.
    Per FR-006: Store JWT in httpOnly cookie.
    Per US2: User login flow.
    """
    user = authenticate_user(
        session=session,
        email=user_data.email,
        password=user_data.password,
    )

    if user is None:
        # Per FR-018, US2: Invalid credentials (same message for security)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"X-Error-Code": ErrorCode.UNAUTHORIZED},
        )

    # Create JWT token
    token = create_access_token(user.id)

    # Set httpOnly cookie
    # Per FR-006: httpOnly prevents JavaScript access
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=settings.jwt_expiration_hours * 3600,
    )

    return UserResponse.model_validate(user)


@router.post(
    "/logout",
    responses={
        200: {"description": "Logged out successfully"},
    },
)
def logout(response: Response) -> dict:
    """Clear JWT cookie and end session.

    Per FR-007: Allow authenticated users to log out, clearing their session.
    Per US2: User logout flow.
    """
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
    )

    return {"message": "Logged out successfully"}
