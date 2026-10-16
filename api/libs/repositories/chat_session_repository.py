from sqlalchemy import select

from libs.database import AsyncSessionLocal
from libs.models.chat_session import ChatSession
from libs.models.message import Message
from libs.models.user import User


async def create_chat_session(user: User, uid: str, label: str, initial_message: str | None) -> ChatSession:
    chat_session = ChatSession(user_id=user.id, uid=uid, label=label, initial_message=initial_message)
    async with AsyncSessionLocal() as db:
        db.add(chat_session)
        await db.commit()
    return chat_session


async def get_history(chat_session: ChatSession) -> list[dict[str, str]]:
    async with AsyncSessionLocal() as db:
        messages = await db.scalars(select(Message).where(Message.chat_session_id == chat_session.id).order_by(Message.id))
    history = []
    if chat_session.initial_message:
        history.append({"role": "assistant", "content": chat_session.initial_message})
    for message in messages:
        if message.question is not None:
            history.append({"role": "user", "content": message.question})
        history.append({"role": "assistant", "content": message.answer})
    return history


async def append_qa_to_session(chat_session: ChatSession, question: str | None, answer: str) -> Message:
    message = Message(user_id=chat_session.user_id, chat_session_id=chat_session.id, question=question, answer=answer)
    async with AsyncSessionLocal() as db:
        db.add(message)
        await db.commit()
    return message
