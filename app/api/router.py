"""API router that includes all endpoint routers."""

from fastapi import APIRouter

router = APIRouter()

# Health check endpoint (basic example)
@router.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
