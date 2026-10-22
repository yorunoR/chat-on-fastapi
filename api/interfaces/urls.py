from fastapi import APIRouter

from interfaces.routers.chat_session.post_chat_session import post_chat_session_router
from interfaces.routers.health.get_health import get_health_router
from interfaces.routers.normal_chat.normal_chat_websocket import normal_chat_websocket_router

health_router = APIRouter(tags=["health"])
health_router.include_router(get_health_router)

chat_session_router = APIRouter(tags=["chat_session"])
chat_session_router.include_router(post_chat_session_router)

normal_chat_router = APIRouter(tags=["normal_chat"])
normal_chat_router.include_router(normal_chat_websocket_router)

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(chat_session_router)
api_router.include_router(normal_chat_router)
