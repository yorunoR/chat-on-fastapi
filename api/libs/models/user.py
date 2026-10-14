from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .timestamp_mixin import TimestampMixin

if TYPE_CHECKING:
    from .message import Message
    from .session import Session


class User(Base, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    uid: Mapped[str] = mapped_column(String(256), unique=True, nullable=True)

    sessions: Mapped[list["Session"]] = relationship(back_populates="user", passive_deletes="all")
    messages: Mapped[list["Message"]] = relationship(back_populates="user", passive_deletes="all")
