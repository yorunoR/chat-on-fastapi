from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from config.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

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
