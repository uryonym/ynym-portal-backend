"""共通レスポンス構造のベーススキーマ."""

from pydantic import BaseModel
from typing import Any, Optional


class SuccessResponse(BaseModel):
    """標準成功レスポンスモデル."""

    data: Any
    message: str = "成功"


class ErrorResponse(BaseModel):
    """標準エラーレスポンスモデル."""

    detail: str
    status_code: int
    error_type: Optional[str] = None
