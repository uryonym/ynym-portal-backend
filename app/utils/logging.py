"""ロギング設定."""

import logging
import sys

from app.core.config import settings

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def setup_logging() -> None:
    """アプリケーション用のロギングを設定."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=_LOG_FORMAT, datefmt=_DATE_FORMAT))

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    # ハンドラーの重複登録を避ける
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # SQLAlchemy のクエリログ（INFO 以下では抑制し DEBUG のみ出力）
    sql_log_level = (
        logging.DEBUG if settings.LOG_LEVEL.upper() == "DEBUG" else logging.WARNING
    )
    logging.getLogger("sqlalchemy.engine").setLevel(sql_log_level)

    # uvicorn アクセスログは独自ミドルウェアに任せるため抑制
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
