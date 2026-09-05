"""ユーザーリポジトリ."""

from typing import Optional

from sqlalchemy import select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """ユーザーに関するデータアクセスを担う."""

    def __init__(self, session) -> None:
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得."""
        stmt = select(User).where(User.email == email)
        return self.session.execute(stmt).scalars().one_or_none()
