"""Vehicle（車）スキーマ."""

from typing import Optional

from pydantic import BaseModel, field_validator


class VehicleCreate(BaseModel):
    """車作成スキーマ.

    Attributes:
        name: 車名（必須、1-255 文字）
        management_number: 管理番号（必須、1-100 文字）
        maker: メーカー（必須、1-100 文字）
        model: 型式（必須、1-100 文字）
        year: 年式（オプション）
        number: ナンバー（オプション、1-50 文字）
        tank_capacity: タンク容量（オプション）
    """

    name: str
    seq: int
    maker: str
    model: str
    year: Optional[int] = None
    number: Optional[str] = None
    tank_capacity: Optional[float] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """車名のバリデーション."""
        if not v or not v.strip():
            raise ValueError("車名は必須項目です")
        if len(v) > 255:
            raise ValueError("車名は 255 文字以内である必要があります")
        return v.strip()

    @field_validator("seq")
    @classmethod
    def validate_seq(cls, v: int) -> int:
        """シーケンスのバリデーション."""
        if v <= 0:
            raise ValueError("シーケンスは正の整数である必要があります")
        return v

    @field_validator("maker")
    @classmethod
    def validate_maker(cls, v: str) -> str:
        """メーカーのバリデーション."""
        if not v or not v.strip():
            raise ValueError("メーカーは必須項目です")
        if len(v) > 100:
            raise ValueError("メーカーは 100 文字以内である必要があります")
        return v.strip()

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """型式のバリデーション."""
        if not v or not v.strip():
            raise ValueError("型式は必須項目です")
        if len(v) > 100:
            raise ValueError("型式は 100 文字以内である必要があります")
        return v.strip()

    @field_validator("number")
    @classmethod
    def validate_number(cls, v: Optional[str]) -> Optional[str]:
        """ナンバーのバリデーション."""
        if v is None:
            return None
        if len(v) > 50:
            raise ValueError("ナンバーは 50 文字以内である必要があります")
        return v.strip() if v else None

    @field_validator("tank_capacity")
    @classmethod
    def validate_tank_capacity(cls, v: Optional[float]) -> Optional[float]:
        """タンク容量のバリデーション."""
        if v is None:
            return None
        if v <= 0:
            raise ValueError("タンク容量は 0 より大きい値である必要があります")
        return v


class VehicleUpdate(BaseModel):
    """車更新スキーマ（すべてのフィールドはオプション）.

    Attributes:
        name: 車名（オプション）
        seq: シーケンス（オプション）
        maker: メーカー（オプション）
        model: 型式（オプション）
        year: 年式（オプション）
        number: ナンバー（オプション）
        tank_capacity: タンク容量（オプション）
    """

    name: Optional[str] = None
    seq: Optional[int] = None
    maker: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    number: Optional[str] = None
    tank_capacity: Optional[float] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """車名のバリデーション."""
        if v is not None:
            if not v.strip():
                raise ValueError("車名は空にできません")
            if len(v) > 255:
                raise ValueError("車名は 255 文字以内である必要があります")
            return v.strip()
        return v

    @field_validator("seq")
    @classmethod
    def validate_seq(cls, v: Optional[int]) -> Optional[int]:
        """シーケンスのバリデーション."""
        if v is not None:
            if v <= 0:
                raise ValueError("シーケンスは正の整数である必要があります")
        return v

    @field_validator("maker")
    @classmethod
    def validate_maker(cls, v: Optional[str]) -> Optional[str]:
        """メーカーのバリデーション."""
        if v is not None:
            if not v.strip():
                raise ValueError("メーカーは空にできません")
            if len(v) > 100:
                raise ValueError("メーカーは 100 文字以内である必要があります")
            return v.strip()
        return v

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: Optional[str]) -> Optional[str]:
        """型式のバリデーション."""
        if v is not None:
            if not v.strip():
                raise ValueError("型式は空にできません")
            if len(v) > 100:
                raise ValueError("型式は 100 文字以内である必要があります")
            return v.strip()
        return v

    @field_validator("number")
    @classmethod
    def validate_number(cls, v: Optional[str]) -> Optional[str]:
        """ナンバーのバリデーション."""
        if v is not None:
            if len(v) > 50:
                raise ValueError("ナンバーは 50 文字以内である必要があります")
            return v.strip() if v else None
        return v

    @field_validator("tank_capacity")
    @classmethod
    def validate_tank_capacity(cls, v: Optional[float]) -> Optional[float]:
        """タンク容量のバリデーション."""
        if v is not None:
            if v <= 0:
                raise ValueError("タンク容量は 0 より大きい値である必要があります")
        return v


class VehicleResponse(BaseModel):
    """車レスポンススキーマ.

    Attributes:
        id: 車 ID
        user_id: ユーザー ID
        name: 車名
        seq: シーケンス
        maker: メーカー
        model: 型式
        year: 年式
        number: ナンバー
        tank_capacity: タンク容量
        created_at: 作成日時（ISO 8601）
        updated_at: 更新日時（ISO 8601）
    """

    id: str
    user_id: str
    name: str
    seq: int
    maker: str
    model: str
    year: Optional[int] = None
    number: Optional[str] = None
    tank_capacity: Optional[float] = None
    created_at: str
    updated_at: str

    class Config:
        """Pydantic 設定."""

        from_attributes = True
