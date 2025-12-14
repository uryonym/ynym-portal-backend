from typing import Optional
from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime

from app.models.base import JST


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(primary_key=True, index=True, default=uuid.uuid4)
    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(nullable=True)
    avatar_url: Optional[str] = Field(nullable=True)
    created_at: datetime = Field(default=datetime.now(JST))
