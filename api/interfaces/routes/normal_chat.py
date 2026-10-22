from fastapi import APIRouter, Depends

from interfaces.dependencies.websocket import track_connection
from interfaces.handlers.normal_chat.normal_chat_websocket import normal_chat_websocket

normal_chat_router = APIRouter(prefix="/ws/normal_chat", tags=["normal_chat"])
normal_chat_router.add_api_websocket_route(
    "/{session_uid}",
    normal_chat_websocket,
    dependencies=[Depends(track_connection)],
)
