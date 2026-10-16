from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from admin.setup import init_admin
from config.settings import BACKGROUND_TASK_SHUTDOWN_TIMEOUT_SECONDS
from interfaces.middleware import setup_middleware
from interfaces.urls import api_router
from libs.database import db_engine
from libs.tasks.background_task import wait_background_tasks


@asynccontextmanager
async def lifespan(_api: FastAPI) -> AsyncGenerator[None]:
    yield
    # 切り離した後処理を、終了時に途中で捨てないよう待つ
    await wait_background_tasks(BACKGROUND_TASK_SHUTDOWN_TIMEOUT_SECONDS)


def create_api() -> FastAPI:
    api = FastAPI(lifespan=lifespan)
    setup_middleware(api)
    api.include_router(api_router)
    init_admin(api, db_engine)
    return api


api = create_api()
