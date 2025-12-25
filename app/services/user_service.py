from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        stmt = select(User).where(User.email == email)
        result = await self.db_session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_or_create(self, user_in: UserCreate) -> User:
        """Get existing user or create new one (upsert by email)."""
        user = await self.get_by_email(email=user_in.email)

        if user:
            user.name = user_in.name
            user.avatar_url = user_in.avatar_url
            self.db_session.add(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)
            return user

        user = User(
            email=user_in.email, name=user_in.name, avatar_url=user_in.avatar_url
        )
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user
