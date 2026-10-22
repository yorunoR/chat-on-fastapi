from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from interfaces.dependencies.http import HttpUser
from libs.repositories.chat_session_repository import create_chat_session

post_chat_session_router = APIRouter()


class CreateChatSessionRequest(BaseModel):
    uid: str = Field(max_length=128)
    label: str = Field(max_length=256)
    initial_message: str | None = None


@post_chat_session_router.post("/api/chat_session", status_code=status.HTTP_204_NO_CONTENT)
async def post_chat_session(
    body: CreateChatSessionRequest,
    user: HttpUser,
) -> None:
    await create_chat_session(
        user=user,
        uid=body.uid,
        label=body.label,
        initial_message=body.initial_message,
    )
