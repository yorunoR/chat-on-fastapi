from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .timestamp_mixin import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    uid: Mapped[str] = mapped_column(String(256), unique=True, nullable=True)
