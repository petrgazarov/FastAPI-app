"""create initial tables

Revision ID: 184d20e99b62
Revises: 
Create Date: 2023-03-31 19:31:13.839153

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "184d20e99b62"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
        ),
        sa.Column(
            "write_key",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            index=True,
            unique=True,
            default=uuid4,
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
    op.create_table(
        "events",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("path", sa.String, nullable=False),
        sa.Column("domain", sa.String, nullable=False),
        sa.Column("provider", sa.String, nullable=False),
        sa.Column(
            # nullable=False does not work correctly with SQLModel
            "properties",
            postgresql.JSONB,
        ),
        sa.Column(
            "account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        index_name="index_events_on_name_and_account_id",
        table_name="events",
        columns=["name", "account_id"],
    )


def downgrade() -> None:
    op.drop_table("events")
    op.drop_table("accounts")
