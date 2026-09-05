"""API エンドポイントパッケージ."""

from .auth import router as auth_router
from .fuel_records import router as fuel_records_router
from .note_categories import router as note_categories_router
from .notes import router as notes_router
from .tasks import router as tasks_router
from .users import router as users_router
from .vehicles import router as vehicles_router

__all__ = [
    "auth_router",
    "fuel_records_router",
    "note_categories_router",
    "notes_router",
    "tasks_router",
    "users_router",
    "vehicles_router",
]
