from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, WebSocket, WebSocketException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import ENV
from db.database import get_db
from libs.models.user import User


async def get_ws_user(
    websocket: WebSocket,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """接続時の認証 (Django の _populate_auth_context 相当)。

    ブラウザの WebSocket はカスタムヘッダーを付けられないため、
    クエリパラメータ ?token=<uid> で受け取る。
    """
    token = websocket.query_params.get("token")
    if not token:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    user = await db.scalar(select(User).where(User.uid == token))
    if user is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return user


async def track_connection(
    user: Annotated[User, Depends(get_ws_user)],
) -> AsyncGenerator[User]:
    """接続数メトリクス (connect / disconnect 相当)。yield 後が disconnect。"""
    if ENV != "local":
        logger.info("ConcurrentConnections +1 user_id={}", user.id)
    try:
        yield user
    finally:
        if ENV != "local":
            logger.info("ConcurrentConnections -1 user_id={}", user.id)


WsUser = Annotated[User, Depends(track_connection)]
