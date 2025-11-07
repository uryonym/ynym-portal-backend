"""FastAPI アプリケーションインスタンスとスタートアップ/シャットダウンイベント."""

from fastapi import FastAPI
from app.config import settings
from app.api.router import router
from app.utils.logging import setup_logging

# ロギング設定
setup_logging()

# FastAPI アプリを作成
app = FastAPI(
    title="ynym Portal Backend",
    description="ynym portal 向け FastAPI バックエンドシステム",
    version="0.1.0",
)

# ルータをマウント
app.include_router(router, prefix="/api")


@app.get("/health")
async def health_check() -> dict:
    """ヘルスチェックエンドポイント."""
    return {"status": "ok", "environment": settings.environment}
