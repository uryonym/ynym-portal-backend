"""ロギング設定."""

import logging
from app.config import settings


def setup_logging() -> None:
    """アプリケーション用のロギングを設定."""
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
