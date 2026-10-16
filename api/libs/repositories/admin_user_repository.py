from sqlalchemy import select

from libs.database import AsyncSessionLocal
from libs.models.admin_user import AdminUser


async def get_admin_user_by_email(email: str) -> AdminUser | None:
    async with AsyncSessionLocal() as db:
        return await db.scalar(select(AdminUser).where(AdminUser.email == email))
