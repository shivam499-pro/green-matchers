# routes/__init__.py
from .auth import router as auth_router
from .users import router as users_router
from .jobs import router as jobs_router
from .careers import router as careers_router
from .translation import router as translation_router
from .system import router as system_router
from .vector import router as vector_router

__all__ = [
    "auth_router",
    "users_router",
    "jobs_router",
    "careers_router",
    "translation_router",
    "system_router",
    "vector_router"
]