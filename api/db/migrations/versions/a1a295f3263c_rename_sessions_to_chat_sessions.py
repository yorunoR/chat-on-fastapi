"""rename_sessions_to_chat_sessions

Revision ID: a1a295f3263c
Revises: 1833f4738460
Create Date: 2026-10-16 10:04:24.086632

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1a295f3263c'
down_revision: Union[str, Sequence[str], None] = '1833f4738460'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # テーブル名の変更は autogenerate では drop / create になるため、rename で書き換えている
    op.rename_table("sessions", "chat_sessions")
    op.execute("ALTER SEQUENCE sessions_id_seq RENAME TO chat_sessions_id_seq")
    op.execute("ALTER TABLE chat_sessions RENAME CONSTRAINT sessions_pkey TO chat_sessions_pkey")
    op.drop_constraint("sessions_uid_key", "chat_sessions", type_="unique")
    op.create_index(op.f("ix_chat_sessions_uid"), "chat_sessions", ["uid"], unique=True)
    op.execute("ALTER TABLE chat_sessions RENAME CONSTRAINT sessions_user_id_fkey TO chat_sessions_user_id_fkey")
    op.add_column("chat_sessions", sa.Column("initial_message", sa.Text(), nullable=True))

    op.alter_column("messages", "session_id", new_column_name="chat_session_id")
    op.execute("ALTER TABLE messages RENAME CONSTRAINT messages_session_id_fkey TO messages_chat_session_id_fkey")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE messages RENAME CONSTRAINT messages_chat_session_id_fkey TO messages_session_id_fkey")
    op.alter_column("messages", "chat_session_id", new_column_name="session_id")

    op.drop_column("chat_sessions", "initial_message")
    op.execute("ALTER TABLE chat_sessions RENAME CONSTRAINT chat_sessions_user_id_fkey TO sessions_user_id_fkey")
    op.drop_index(op.f("ix_chat_sessions_uid"), table_name="chat_sessions")
    op.create_unique_constraint("sessions_uid_key", "chat_sessions", ["uid"])
    op.execute("ALTER TABLE chat_sessions RENAME CONSTRAINT chat_sessions_pkey TO sessions_pkey")
    op.execute("ALTER SEQUENCE chat_sessions_id_seq RENAME TO sessions_id_seq")
    op.rename_table("chat_sessions", "sessions")
