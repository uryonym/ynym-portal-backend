"""FastAPI アプリケーションインスタンスとスタートアップ/シャットダウンイベント."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.middleware.logging import LoggingMiddleware
from app.utils.logging import setup_logging
from .routers import (
    auth_router,
    fuel_records_router,
    note_categories_router,
    notes_router,
    tasks_router,
    users_router,
    vehicles_router,
)

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
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(vehicles_router)
app.include_router(fuel_records_router)
app.include_router(note_categories_router)
app.include_router(notes_router)
