"""Base schemas for common response structures."""

from pydantic import BaseModel
from typing import Any, Optional


class SuccessResponse(BaseModel):
    """Standard success response model."""

    data: Any
    message: str = "Success"


class ErrorResponse(BaseModel):
    """Standard error response model."""

    detail: str
    status_code: int
    error_type: Optional[str] = None
