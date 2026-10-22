from fastapi import APIRouter

from interfaces.handlers.health.get_health import get_health

health_router = APIRouter(prefix="/health", tags=["health"])
health_router.add_api_route("", get_health, methods=["GET"])
