"""FastAPI application instance and startup/shutdown events."""

from fastapi import FastAPI
from app.config import settings
from app.api.router import router
from app.utils.logging import setup_logging

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="ynym Portal Backend",
    description="FastAPI backend system for ynym portal",
    version="0.1.0",
)

# Include routers
app.include_router(router, prefix="/api")


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "environment": settings.environment}
