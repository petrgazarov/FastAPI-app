"""create event_documentation_examples table

Revision ID: 69df1b9d2b1a
Revises: 411e9f5bac7a
Create Date: 2023-05-01 05:00:08.598507

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "69df1b9d2b1a"
down_revision = "411e9f5bac7a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "event_documentation_examples",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
        ),
        sa.Column(
            "event_documentation_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("event_documentations.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "event_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("events.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
            unique=True,
        ),
        sa.Column(
            "account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "created_at", sa.DateTime, server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("event_documentation_examples")
