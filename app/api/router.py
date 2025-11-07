"""すべてのエンドポイントルータを含む API ルータ."""

from fastapi import APIRouter

router = APIRouter()

# ヘルスチェックエンドポイント（基本的な例）
@router.get("/health")
async def health() -> dict:
    """ヘルスチェックエンドポイント."""
    return {"status": "ok"}
