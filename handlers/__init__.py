from .commands import router as commands_router
from .profile_buttons import router as profile_router
from .message import router as messages_router
from .callbacks import router as callback_router

__all__ = [
    "commands_router",
    "profile_router",
    "messages_router",
    "callback_router",
]
