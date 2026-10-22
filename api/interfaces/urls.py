from fastapi import APIRouter, Depends, status

from interfaces.dependencies.websocket import track_connection
from interfaces.handlers.chat_session.post_chat_session import post_chat_session
from interfaces.handlers.health.get_health import get_health
from interfaces.handlers.normal_chat.normal_chat_websocket import normal_chat_websocket

api_router = APIRouter()

api_router.add_api_route("/health", get_health, methods=["GET"], tags=["health"])

api_router.add_api_route(
    "/api/chat_session",
    post_chat_session,
    methods=["POST"],
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["chat_session"],
)

api_router.add_api_websocket_route(
    "/ws/normal_chat/{session_uid}",
    normal_chat_websocket,
    dependencies=[Depends(track_connection)],
)
