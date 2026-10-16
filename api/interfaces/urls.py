from fastapi import APIRouter

from interfaces.routers import chat_session, health, normal_chat

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(chat_session.router, tags=["chat_session"])
api_router.include_router(normal_chat.router, tags=["normal_chat"])
