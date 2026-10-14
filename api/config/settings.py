import os

DB_USER = os.environ.get("DB_USER", "developer")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "api_dev")

ENV = os.environ.get("ENV", "local")
