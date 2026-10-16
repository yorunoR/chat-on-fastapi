from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    flow_name: Mapped[str] = mapped_column(String(128), nullable=False)
    node_name: Mapped[str] = mapped_column(String(128), nullable=False)
    agent_name: Mapped[str] = mapped_column(String(128), nullable=True)

    template: Mapped[dict] = mapped_column(JSONB, nullable=True)
    hexdigest: Mapped[str] = mapped_column(String(128), nullable=True)
