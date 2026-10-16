from sqlalchemy import select

from libs.database import AsyncSessionLocal
from libs.models.user import User


async def get_user_by_uid(uid: str) -> User | None:
    async with AsyncSessionLocal() as db:
        return await db.scalar(select(User).where(User.uid == uid))
