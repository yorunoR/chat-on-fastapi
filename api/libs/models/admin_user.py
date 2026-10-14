from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .timestamp_mixin import TimestampMixin


class AdminUser(Base, TimestampMixin):
    __tablename__ = "admin_users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
