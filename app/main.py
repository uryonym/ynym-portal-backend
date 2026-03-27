"""FastAPI アプリケーションインスタンスとスタートアップ/シャットダウンイベント."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.router import router
from app.middleware.logging import LoggingMiddleware
from app.utils.logging import setup_logging
from app.utils.exceptions import ApplicationException

# ロギング設定
setup_logging()

# FastAPI アプリを作成
app = FastAPI(
    title="ynym Portal Backend",
    description="ynym portal 向け FastAPI バックエンドシステム",
    version="0.1.0",
)

# CORS ミドルウェア設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# HTTP リクエストロギングミドルウェア
app.add_middleware(LoggingMiddleware)

# ルータをマウント
app.include_router(router, prefix="/api")


@app.exception_handler(ApplicationException)
async def application_exception_handler(
    request: Request, exc: ApplicationException
) -> JSONResponse:
    """カスタム例外を HTTP レスポンスに変換."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.get("/health")
def health_check() -> dict:
    """ヘルスチェックエンドポイント."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}
