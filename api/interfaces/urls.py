from fastapi import APIRouter

from interfaces.routers import health, normal_chat

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(normal_chat.router, tags=["normal_chat"])
