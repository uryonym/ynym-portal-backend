"""すべてのエンドポイントルータを含む API ルータ."""

from fastapi import APIRouter

from app.api.endpoints import fuel_records, tasks, vehicles, auth, users

router = APIRouter()


# ヘルスチェックエンドポイント（基本的な例）
@router.get("/health")
async def health() -> dict:
    """ヘルスチェックエンドポイント."""
    return {"status": "ok"}


# 認証エンドポイントを登録
router.include_router(auth.router)

# ユーザーエンドポイントを登録
router.include_router(users.router)

# タスクエンドポイントを登録
router.include_router(tasks.router)

# 車エンドポイントを登録
router.include_router(vehicles.router)

# 燃費記録エンドポイントを登録
router.include_router(fuel_records.router)
