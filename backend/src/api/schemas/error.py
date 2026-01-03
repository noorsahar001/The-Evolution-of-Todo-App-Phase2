"""Error response schema.

Per FR-021: API MUST return 400 Bad Request for validation errors with descriptive messages.
Per FR-022: API MUST return responses in JSON format.
Per Constitution IX: Error responses MUST follow a consistent structure.
"""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response format.

    Per Constitution IX:
    {
        "detail": "Human-readable error message",
        "code": "ERROR_CODE"
    }
    """

    detail: str
    code: str


# Error codes as constants
class ErrorCode:
    """Standard error codes per spec."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
