from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .timestamp_mixin import TimestampMixin
from .user import User

if TYPE_CHECKING:
    from .message import Message


class ChatSession(Base, TimestampMixin):
    __tablename__ = "chat_sessions"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="chat_sessions")

    label: Mapped[str] = mapped_column(String(256), nullable=False)
    uid: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    initial_message: Mapped[str] = mapped_column(Text, nullable=True)

    messages: Mapped[list["Message"]] = relationship(back_populates="chat_session", passive_deletes="all")
