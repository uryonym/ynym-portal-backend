"""すべてのエンドポイントルータを含む API ルータ."""

from fastapi import APIRouter

from app.api.endpoints import tasks

router = APIRouter()

# ヘルスチェックエンドポイント（基本的な例）
@router.get("/health")
async def health() -> dict:
    """ヘルスチェックエンドポイント."""
    return {"status": "ok"}


# タスクエンドポイントを登録
router.include_router(tasks.router)
