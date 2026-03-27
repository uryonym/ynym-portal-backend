"""ユーザー管理サービス."""

from __future__ import annotations

from typing import Optional

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """ユーザー管理ビジネスロジック層."""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def get_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得."""
        return self.user_repo.get_by_email(email)

    def get_or_create(self, user_in: UserCreate) -> User:
        """メールアドレスでユーザーを取得、存在しない場合は作成（upsert）."""
        user = self.get_by_email(user_in.email)
        if user:
            user.name = user_in.name
            user.avatar_url = user_in.avatar_url
            return self.user_repo.save(user)
        user = User(
            email=user_in.email,
            name=user_in.name,
            avatar_url=user_in.avatar_url,
        )
        return self.user_repo.save(user)
