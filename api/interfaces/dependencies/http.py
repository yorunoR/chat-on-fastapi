from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from libs.database import get_db
from libs.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


async def get_http_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """HTTP リクエストの認証。Authorization: Bearer <uid> で受け取る。"""
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await db.scalar(select(User).where(User.uid == credentials.credentials))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


HttpUser = Annotated[User, Depends(get_http_user)]
