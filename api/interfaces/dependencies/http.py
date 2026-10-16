from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from libs.models.user import User
from libs.repositories.user_repository import get_user_by_uid

bearer_scheme = HTTPBearer(auto_error=False)


async def get_http_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    """HTTP リクエストの認証。Authorization: Bearer <uid> で受け取る。"""
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await get_user_by_uid(credentials.credentials)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


HttpUser = Annotated[User, Depends(get_http_user)]
