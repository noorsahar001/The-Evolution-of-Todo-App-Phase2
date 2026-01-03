"""JWT token creation and verification.

Per FR-005: System MUST issue a JWT token upon successful login.
Per FR-006: System MUST store JWT in httpOnly cookie.
Per FR-017: All task endpoints MUST require valid JWT authentication.
Per Constitution VII: JWT Validation - Every request MUST validate the JWT token.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hashed password

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Create a JWT access token for a user.

    Args:
        user_id: The user's database ID

    Returns:
        Encoded JWT token string
    """
    expire = datetime.now(timezone.utc) + timedelta(
        hours=settings.jwt_expiration_hours
    )
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[int]:
    """Verify a JWT token and extract the user ID.

    Per Constitution VII: Backend MUST NOT trust any user ID from frontend;
    extract from JWT only.

    Args:
        token: JWT token string

    Returns:
        User ID if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            return None
        return int(user_id_str)
    except (JWTError, ValueError):
        return None
