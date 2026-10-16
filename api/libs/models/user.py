from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .timestamp_mixin import TimestampMixin

if TYPE_CHECKING:
    from .chat_session import ChatSession
    from .message import Message


class User(Base, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    uid: Mapped[str] = mapped_column(String(256), unique=True, nullable=True)

    chat_sessions: Mapped[list["ChatSession"]] = relationship(back_populates="user", passive_deletes="all")
    messages: Mapped[list["Message"]] = relationship(back_populates="user", passive_deletes="all")
