from collections.abc import AsyncGenerator

from loguru import logger

from config.settings import ENV


async def track_connection() -> AsyncGenerator[None]:
    """接続数メトリクス (connect / disconnect 相当)。yield 後が disconnect。"""
    if ENV != "local":
        logger.info("ConcurrentConnections +1")
    try:
        yield
    finally:
        if ENV != "local":
            logger.info("ConcurrentConnections -1")
