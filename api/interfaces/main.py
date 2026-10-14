from fastapi import FastAPI

from admin.setup import init_admin
from db.database import db_engine
from interfaces.middleware import setup_middleware
from interfaces.urls import api_router


def create_api() -> FastAPI:
    api = FastAPI()
    setup_middleware(api)
    api.include_router(api_router)
    init_admin(api, db_engine)
    return api


api = create_api()
