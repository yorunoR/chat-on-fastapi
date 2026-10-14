from fastapi import APIRouter

from interfaces.routers import health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
