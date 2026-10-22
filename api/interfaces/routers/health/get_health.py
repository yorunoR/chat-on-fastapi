from fastapi import APIRouter

get_health_router = APIRouter()


@get_health_router.get("/health")
async def get_health() -> dict[str, str]:
    return {"status": "ok"}
