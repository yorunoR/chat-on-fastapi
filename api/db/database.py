import os
from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

DB_USER = os.environ.get("DB_USER", "developer")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "api_dev")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SYNC_DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db_engine = create_async_engine(
    DB_URL,
    echo=False,
    future=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=db_engine,
    autoflush=False,
    expire_on_commit=False,
)

sync_db_engine = create_engine(SYNC_DB_URL, echo=False)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=sync_db_engine)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
