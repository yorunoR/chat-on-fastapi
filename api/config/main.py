from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from admin.setup import init_admin
from db.database import db_engine

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_admin(api, db_engine)
