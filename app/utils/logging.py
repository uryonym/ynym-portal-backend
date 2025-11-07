"""Logging configuration."""

import logging
from app.config import settings


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
