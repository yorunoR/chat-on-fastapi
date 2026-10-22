from fastapi import APIRouter

from interfaces.routes.chat_session import chat_session_router
from interfaces.routes.health import health_router
from interfaces.routes.normal_chat import normal_chat_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(chat_session_router)
api_router.include_router(normal_chat_router)
