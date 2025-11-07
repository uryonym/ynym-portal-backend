"""Database models base configuration."""

from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class TimestampModel(SQLModel):
    """Base model with timestamp fields."""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
