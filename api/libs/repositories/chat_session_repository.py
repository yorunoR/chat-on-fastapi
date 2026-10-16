from libs.database import AsyncSessionLocal
from libs.models.chat_session import ChatSession
from libs.models.user import User


async def create_chat_session(user: User, uid: str, label: str, initial_message: str | None) -> ChatSession:
    chat_session = ChatSession(user_id=user.id, uid=uid, label=label, initial_message=initial_message)
    async with AsyncSessionLocal() as db:
        db.add(chat_session)
        await db.commit()
    return chat_session
