from fastapi import APIRouter, status

from interfaces.handlers.chat_session.post_chat_session import post_chat_session

chat_session_router = APIRouter(prefix="/api/chat_session", tags=["chat_session"])
chat_session_router.add_api_route("", post_chat_session, methods=["POST"], status_code=status.HTTP_204_NO_CONTENT)
