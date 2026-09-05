"""リポジトリ基底クラス."""

from typing import Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """汎用リポジトリ基底クラス."""

    def __init__(self, session: Session, model: type[T]) -> None:
        self.session = session
        self.model = model

    def get_by_id(self, id: UUID) -> Optional[T]:
        """ID でエンティティを取得."""
        return self.session.get(self.model, id)

    def save(self, entity: T) -> T:
        """エンティティを保存（insert or update）してリフレッシュ."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        """エンティティを物理削除."""
        self.session.delete(entity)
        self.session.commit()
